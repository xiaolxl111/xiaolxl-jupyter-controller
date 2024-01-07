import subprocess

# 获取默认分支名字
def get_git_main_b_name(path):
    output = subprocess.check_output(
        ['git', 'ls-remote', '--symref', 'origin', 'HEAD'],
        cwd=path
    ).strip().decode('utf-8')

    # Get the branch name from the output
    return  output.split('/')[-1].split('\t')[0]

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
    output = subprocess.check_output(
        ['git', 'ls-remote', '--heads', 'origin'],
        cwd=path
    ).strip().decode('utf-8')

    main_b_name = get_git_main_b_name(path)
    
    for line in output.split('\n'):
        branch_name = line.split('/')[-1]
        
        if main_b_name == branch_name:
            item = {'branch_name':branch_name,'is_main':1}
        else:
            item = {'branch_name':branch_name,'is_main':0}
        
        data.append(item)
    
    return data

# 获取当前分支名字
def get_git_nov_b_name(path):
    return subprocess.check_output(
        ['git', 'rev-parse', '--abbrev-ref', 'HEAD@{upstream}'],
        cwd=path
    ).strip().decode('utf-8').split('/')[1]

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
def get_git_newest_v_sha(path, branch='master'):
    # Fetch the latest commits from all remotes
    subprocess.run(['git', 'fetch', '--all'], cwd=path)
    
    # Get the latest commit SHA of the specified branch
    output = subprocess.check_output(
        ['git', 'rev-parse', f'origin/{branch}'],
        cwd=path
    ).strip()

    # Convert the output to a string
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
def get_git_newest_v_time(path, branch='master'):
    # Get the newest commit SHA
    newest_sha = get_git_newest_v_sha(path, branch)

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
        # Fetch latest remote changes
        subprocess.run(
            ['git', 'fetch', '--all'],
            cwd=git_path
        )
        
        # Checkout the specified branch
        subprocess.run(
            ['git', 'branch','--set-upstream-to=origin/' + branch_name, 'HEAD'],
            cwd=git_path
        )
        
        subprocess.run(
            ['git', 'reset', '--hard', 'origin/' + branch_name],
            cwd=git_path
        )
        subprocess.run(
            ['git', 'pull'],
            cwd=git_path
        )

# 强制覆盖更新
def force_update_git_repo(path):
    # Fetch all remote changes
    subprocess.run(
        ['git', 'fetch', '--all'],
        cwd=path
    )

    # Reset hard to the latest version of the current branch
    subprocess.run(
        ['git', 'reset', '--hard', 'origin'],
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