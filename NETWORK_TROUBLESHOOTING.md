# GitHub网络连接问题解决方案

## 问题描述
```
unable to access 'https://github.com/tuomashi20/pdf-decrypt-mcp.git/': Failed to connect to github.com port 443 after 21119 ms: Could not connect to server
```

## 🔧 解决方案

### 方案1: 检查网络连接
```bash
# 测试GitHub连接
ping github.com

# 测试HTTPS连接
curl -I https://github.com

# 检查DNS解析
nslookup github.com
```

### 方案2: 使用SSH连接（推荐）
SSH连接通常更稳定，特别是在网络受限的环境中。

#### 2.1 生成SSH密钥
```bash
# 生成新的SSH密钥
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# 启动SSH代理
eval "$(ssh-agent -s)"

# 添加SSH密钥到代理
ssh-add ~/.ssh/id_rsa
```

#### 2.2 添加SSH密钥到GitHub
1. 复制公钥内容：
```bash
cat ~/.ssh/id_rsa.pub
```

2. 访问 https://github.com/settings/keys
3. 点击 "New SSH key"
4. 粘贴公钥内容
5. 保存

#### 2.3 使用SSH URL
```bash
# 移除现有的HTTPS远程地址
git remote remove origin

# 添加SSH远程地址
git remote add origin git@github.com:tuomashi20/pdf-decrypt-mcp.git

# 推送代码
git push -u origin main
```

### 方案3: 配置代理
如果您使用代理服务器，请配置Git代理：

```bash
# 设置HTTP代理
git config --global http.proxy http://proxy.company.com:8080
git config --global https.proxy https://proxy.company.com:8080

# 或者设置SOCKS代理
git config --global http.proxy socks5://127.0.0.1:1080
git config --global https.proxy socks5://127.0.0.1:1080
```

### 方案4: 修改DNS设置
```bash
# 使用公共DNS
echo "nameserver 8.8.8.8" > /etc/resolv.conf
echo "nameserver 8.8.4.4" >> /etc/resolv.conf

# Windows下修改网络适配器DNS设置
# 控制面板 → 网络和Internet → 网络和共享中心 → 更改适配器设置
```

### 方案5: 使用GitHub Desktop
如果Git命令行工具无法使用，可以尝试：
1. 下载并安装 GitHub Desktop
2. 登录您的GitHub账户
3. 选择 "Add an Existing Repository from your hard drive"
4. 选择项目文件夹
5. 通过界面进行推送

### 方案6: 手动上传文件
如果所有方法都失败，可以：
1. 在GitHub上创建空仓库
2. 下载ZIP文件
3. 通过GitHub界面上传文件

## 🌍 地区特定解决方案

### 中国大陆用户
```bash
# 使用镜像站点
git config --global url."https://gitclone.com/github.com/".insteadOf "https://github.com/"

# 或者使用GitHub镜像
git remote set-url origin https://github.com.cnpmjs.org/tuomashi20/pdf-decrypt-mcp.git
```

### 企业网络环境
1. 联系IT部门开放GitHub访问权限
2. 使用企业代理设置
3. 考虑使用企业内部的Git仓库

## 📋 测试连接

### 测试HTTPS连接
```bash
curl -v https://github.com
```

### 测试SSH连接
```bash
ssh -T git@github.com
```

### 测试Git连接
```bash
git ls-remote https://github.com/tuomashi20/pdf-decrypt-mcp.git
```

## 🔄 重置Git配置

如果需要重置Git配置：
```bash
# 重置所有Git配置
git config --global --unset-all http.proxy
git config --global --unset-all https.proxy

# 或者重置所有配置
git config --global --unset-all
```

## 📞 获取帮助

如果问题仍然存在：
1. 检查防火墙设置
2. 联系网络管理员
3. 尝试使用其他网络环境
4. 查看GitHub状态页面：https://www.githubstatus.com/

## 🎯 推荐方案

基于您的环境，我推荐以下顺序尝试：

1. **首先尝试SSH连接** - 最稳定可靠
2. **检查网络设置** - 确保基础网络正常
3. **配置代理** - 如果在企业网络中
4. **使用镜像** - 如果在受限地区
5. **手动上传** - 最后的备选方案

---

**注意**: 如果您在中国大陆，建议使用SSH连接或配置代理，这通常能解决大部分连接问题。