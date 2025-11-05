#!/usr/bin/env python3

import csv
import getopt
import os
import sys
from datetime import datetime

import git


def count_diff_lines(diff_text):
    """统计 diff 文本中的插入和删除行数"""
    if not diff_text:
        return 0, 0

    insertions = 0
    deletions = 0

    for line in diff_text.split('\n'):
        if line.startswith('+') and not line.startswith('+++'):
            insertions += 1
        elif line.startswith('-') and not line.startswith('---'):
            deletions += 1

    return insertions, deletions


def format_stat_line(filename, insertions, deletions):
    """格式化单个文件的统计信息"""
    if insertions == 0 and deletions == 0:
        return f"{filename} | 0"
    elif insertions > 0 and deletions == 0:
        return f"{filename} | {insertions} +"
    elif insertions == 0 and deletions > 0:
        return f"{filename} | {deletions} -"
    else:
        # 如果插入和删除都有，使用 +- 格式
        # 格式：filename | N +-，其中 N 是总变更行数
        return f"{filename} | {insertions + deletions} +-"


def get_changed_files(commit):
    """获取提交中变更的文件列表，格式类似 git log --stat"""
    file_stats = []
    total_insertions = 0
    total_deletions = 0
    total_files = 0

    try:
        # 获取父提交
        if commit.parents:
            parent = commit.parents[0]
            # 比较父提交和当前提交的差异
            diff = parent.diff(commit, create_patch=True)

            for item in diff:
                change_type = item.change_type
                filename = None
                insertions = 0
                deletions = 0

                # 获取统计信息：从 diff 文本中统计
                diff_text = None
                if hasattr(item, 'diff') and item.diff:
                    diff_text = item.diff.decode('utf-8', errors='ignore') if isinstance(item.diff, bytes) else str(
                        item.diff)
                    if diff_text:
                        insertions, deletions = count_diff_lines(diff_text)

                if change_type == 'A':
                    # 新增文件
                    filename = item.b_path
                elif change_type == 'D':
                    # 删除文件
                    filename = item.a_path
                elif change_type == 'R':
                    # 重命名文件
                    filename = f"{item.a_path} -> {item.b_path}"
                elif change_type == 'C':
                    # 复制文件
                    filename = f"{item.a_path} -> {item.b_path}"
                elif change_type == 'M':
                    # 修改文件
                    filename = item.b_path if item.b_path else item.a_path
                else:
                    # 其他类型
                    filename = item.b_path if item.b_path else item.a_path

                if filename:
                    file_stats.append((filename, insertions, deletions))
                    total_insertions += insertions
                    total_deletions += deletions
                    total_files += 1
        else:
            # 初始提交，获取所有文件
            for item in commit.tree.traverse():
                if item.type == 'blob':
                    filename = item.path
                    # 尝试获取文件内容来统计行数
                    try:
                        blob = commit.tree[item.path]
                        content = blob.data_stream.read()
                        if isinstance(content, bytes):
                            content = content.decode('utf-8', errors='ignore')
                        # 统计文件行数
                        insertions = len(content.splitlines())
                        if insertions == 0 and len(content) > 0:
                            insertions = 1
                    except:
                        insertions = 1

                    file_stats.append((filename, insertions, 0))
                    total_insertions += insertions
                    total_files += 1

        # 格式化输出
        lines = []
        for filename, ins, dels in file_stats:
            lines.append(format_stat_line(filename, ins, dels))

        # 添加总体统计
        if total_files > 0:
            stats_line = f"{total_files} file"
            if total_files > 1:
                stats_line += "s"
            stats_line += " changed"

            if total_insertions > 0 or total_deletions > 0:
                parts = []
                if total_insertions > 0:
                    parts.append(f"{total_insertions} insertion")
                    if total_insertions > 1:
                        parts[-1] += "s"
                    parts[-1] += "(+)"
                if total_deletions > 0:
                    parts.append(f"{total_deletions} deletion")
                    if total_deletions > 1:
                        parts[-1] += "s"
                    parts[-1] += "(-)"
                stats_line += ", " + ", ".join(parts)

            lines.append(stats_line)

        return '\n'.join(lines) if lines else ''

    except Exception as e:
        # 如果获取文件列表失败，返回空字符串
        return ''


def export_git_log_to_csv(repo_path, output_file, max_count=None):
    """
    导出 git log 到 CSV 文件
    
    Args:
        repo_path: Git 仓库路径（默认为当前目录）
        output_file: 输出 CSV 文件路径
        max_count: 最大提交数量（None 表示全部）
    """
    try:
        repo = git.Repo(repo_path)
    except git.InvalidGitRepositoryError:
        print(f"错误: {repo_path} 不是一个有效的 Git 仓库")
        sys.exit(1)

    # 准备 CSV 数据
    csv_data = []

    # 获取提交列表
    commits = list(repo.iter_commits(max_count=max_count))

    print(f"正在处理 {len(commits)} 个提交...")

    for commit in commits:
        # 缩写提交哈希
        short_hash = commit.hexsha[:7]

        # 作者信息
        author_name = commit.author.name
        author_email = commit.author.email

        # 作者日期
        author_date = datetime.fromtimestamp(commit.authored_date).strftime('%Y-%m-%d %H:%M:%S')

        # 提交信息
        subject = commit.message if commit.message else ''

        # 变更的文件列表（已经是格式化字符串）
        files_str = get_changed_files(commit)

        csv_data.append([
            short_hash,
            author_name,
            author_email,
            author_date,
            subject,
            files_str
        ])

    # 写入 CSV 文件
    csv_headers = ['提交哈希', '作者姓名', '作者邮箱', '作者日期', '提交信息', '变更文件列表']

    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(csv_headers)
            writer.writerows(csv_data)
        print(f"成功导出 {len(csv_data)} 条记录到 {output_file}")
    except Exception as e:
        print(f"错误: 写入 CSV 文件失败 - {e}")
        sys.exit(1)


def main():
    """主函数"""
    repo_path = '.'
    output_file = 'git_log.csv'
    max_count = None

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hr:o:n:",
            ["help", "repo=", "output=", "number="]
        )
    except getopt.GetoptError:
        print_usage()
        sys.exit(1)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_usage()
            sys.exit()
        elif opt in ("-r", "--repo"):
            repo_path = arg
        elif opt in ("-o", "--output"):
            output_file = arg
        elif opt in ("-n", "--number"):
            try:
                max_count = int(arg)
            except ValueError:
                print("错误: -n/--number 参数必须是整数")
                sys.exit(1)

    export_git_log_to_csv(repo_path, output_file, max_count)


def print_usage():
    """打印使用说明"""
    usage = """
用法: {} [选项]

选项:
  -h, --help           显示帮助信息
  -r, --repo PATH      Git 仓库路径（默认为当前目录）
  -o, --output FILE    输出 CSV 文件路径（默认为 git_log.csv）
  -n, --number N       最多导出的提交数量（默认导出全部）

示例:
  {}                           # 导出当前目录的 git log
  {} -r /path/to/repo         # 导出指定仓库的 git log
  {} -o output.csv            # 指定输出文件名
  {} -n 100                   # 只导出最近 100 个提交
  {} -r /path/to/repo -o output.csv -n 50  # 组合使用
""".format(
        sys.argv[0], sys.argv[0], sys.argv[0],
        sys.argv[0], sys.argv[0], sys.argv[0]
    )
    print(usage)


if __name__ == "__main__":
    main()
