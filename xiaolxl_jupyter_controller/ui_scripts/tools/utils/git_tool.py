import subprocess

# 获取默认分支名字
def get_git_main_b_name(path):
    # 使用 subprocess 调用 git 命令获取当前分支名
    output = subprocess.check_output(
        ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
        cwd=path
    ).strip().decode('utf-8')

    # 直接返回获取到的分支名
    return output

# 远程仓库地址
def get_git_main_url(path):
    output = subprocess.check_output(
        ['git', 'ls-remote', '--get-url', 'origin'],
        cwd=path
    ).strip().decode('utf-8')

    # Get the branch name from the output
    return output

# 获取全部分支名字
def get_git_all_b_name(path):
    data = []
    # 获取所有远程分支名
    output = subprocess.check_output(
        ['git', 'branch', '-r'],
        cwd=path
    ).strip().decode('utf-8')

    # 获取主分支名
    main_b_name = get_git_main_b_name(path)
    
    # 遍历输出的每一行，解析出分支名
    for line in output.split('\n'):
        # 跳过包含 'HEAD ->' 的行
        if 'HEAD ->' in line:
            continue

        # 使用 replace 方法去除 'origin/' 前缀，确保只替换第一次出现的 'origin/'
        branch_name = line.strip().replace('origin/', '', 1)

        # 检查当前分支是否是主分支
        if main_b_name == branch_name:
            item = {'branch_name': branch_name, 'is_main': 1}
        else:
            item = {'branch_name': branch_name, 'is_main': 0}
        
        # 将分支信息添加到列表中
        data.append(item)
    
    return data

# 获取当前分支名字
def get_git_nov_b_name(path):
    # 获取当前分支的完整名字
    branch_name = subprocess.check_output(
        ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
        cwd=path
    ).strip().decode('utf-8')

    # 直接返回分支名，不需要再进行分割
    return branch_name

# 获取当前分支当前版本SHA
def get_git_now_v_sha(path):
    output = subprocess.check_output(
        ['git', 'rev-parse', 'HEAD'],
        cwd=path
    ).strip()

    # Convert the output to a string
    output = output.decode('utf-8')

    # Remove the extra content
    full_sha = output.split('/')[0]
    
    return full_sha

# 获取当前分支最新版本SHA
def get_git_newest_v_sha(path):
    # 获取当前分支名
    current_branch = subprocess.check_output(
        ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
        cwd=path
    ).strip().decode('utf-8')

    # 从所有远程获取最新提交
    subprocess.run(['git', 'fetch', '--all'], cwd=path)
    
    # 获取当前分支最新提交的 SHA
    output = subprocess.check_output(
        ['git', 'rev-parse', f'origin/{current_branch}'],
        cwd=path
    ).strip()

    # 将输出转换为字符串
    sha = output.decode('utf-8')
    
    return sha

# 获取当前版本时间
def get_git_now_v_time(path):
    now_sha = get_git_now_v_sha(path)

    date = subprocess.check_output(
        ['git', 'show', '-s', '--format=%ci', now_sha],
        cwd=path
    ).decode('utf-8').strip()
    
    dates = date.split(" ")
    
    out_data = dates[0] + " " + dates[1]
    
    return out_data

# 获取最新版本时间
def get_git_newest_v_time(path):
    # Get the newest commit SHA
    newest_sha = get_git_newest_v_sha(path)

    # Get the commit date
    date = subprocess.check_output(
        ['git', 'show', '-s', '--format=%ci', newest_sha],
        cwd=path
    ).decode('utf-8').strip()
    
    # Extract and format the date
    dates = date.split(" ")
    out_date = dates[0] + " " + dates[1]
    
    return out_date

# 切换分支与版本
def change_git_b_and_v(path,branch_name,full_sha):
    git_path = path

    if full_sha != "":
        # Fetch latest remote changes
        subprocess.run(
            ['git', 'fetch', '--all'],
            cwd=git_path
        )

        # Checkout the specified branch
        # subprocess.run(
        #     ['git', 'checkout','-b', branch_name],
        #     cwd=git_path
        # )

        # Update Branch
        subprocess.run(
            ['git', 'pull'],
            cwd=git_path
        )

        # Reset to the specified version
        subprocess.run(
            ['git', 'reset', '--hard', full_sha],
            cwd=git_path
        )
        
        # Update Branch
        # subprocess.run(
        #     ['git', 'pull'],
        #     cwd=git_path
        # )
    else:
        # Fetch the latest changes from all remotes
        subprocess.run(['git', 'fetch', '--all'], cwd=git_path)

        # Switch to the specified branch (this will automatically set up tracking if the branch tracks a remote branch)
        subprocess.run(['git', 'switch', branch_name], cwd=git_path)

        # Reset the branch to the state of the remote branch, discarding any local changes
        subprocess.run(['git', 'reset', '--hard', 'origin/' + branch_name], cwd=git_path)

# 强制覆盖更新
def force_update_git_repo(path):
    now_b_name = get_git_nov_b_name(path)

    # Fetch all remote changes
    subprocess.run(
        ['git', 'fetch', '--all'],
        cwd=path
    )

    # Switch to the specified branch (this will automatically set up tracking if the branch tracks a remote branch)
    subprocess.run(['git', 'switch', now_b_name], cwd=path)

    # Reset hard to the latest version of the current branch
    subprocess.run(
        ['git', 'reset', '--hard', 'origin/' + now_b_name],
        cwd=path
    )

    # Pull the latest changes
    subprocess.run(
        ['git', 'pull'],
        cwd=path
    )
    
    # git clean -fd
    subprocess.run(
        ['git', 'clean', '-fd'],
        cwd=path
    )