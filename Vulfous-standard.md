# Vulfocus 环境信息规范

未解决 Vulfocus 漏洞环境相关命名不一致问题，现在通过该方案来解决问题。另外，依据约束力强弱及故障敏感性，规约依次分为【重要】、【强制】、【推荐】、【参考】四大类。在延伸信息中，“说明”对规约做了适当扩展和解释; “正例”提倡什么样的编码和实现方式；“反例”说明需要提防的雷区，以及真实的错误案例。


| 版本号 | 制定团队      | 修改/制定人 | 更新时间   | 备注                           |
| ------ | ------------- | ----------- | ---------- | ------------------------------ |
| 1.0.0  | Vulfocus 团队 | r4v3zn      | 2021-06-09 | 首次发布 Vulfocus 环境信息规范 |


## 漏洞名称

1. **【重要】**漏洞名称命名规则：系统名称+漏洞类型+（漏洞编号）。

正例：

```
Weblogic 远程命令执行（CVE-2020-2883）
Tomcat 文件包含（CVE-2020-1938）
Tomcat 任意写入文件漏洞（CVE-2017-12615）
```

2. **【重要】**英文与中文之间必须通过“空格”分割。

正例：

```
Weblogic 远程命令执行（CVE-2020-2883）
```

反例：

```
Weblogic远程命令执行（CVE-2020-2883）
```

3. **【强制】**漏洞编号中的括号必须为`（）`中文括号。

## 漏洞描述

1. **【重要】**漏洞描述规则：产品简介+（换行）+漏洞细节（如没有漏洞细节用漏洞危害替代）+（换行）+备注（描述环境的特殊信息如登陆信息或这特殊URL等内容）三部分组成，描述完毕一段内容时必须换行。

正例：

```
DokuWiki是德国软件开发者Andreas Gohr所研发的一款基于PHP的Wiki引擎，它主要用于中小团队和个人网站知识库的管理，并提供版本控制、全文检索和权限控制等功能。
DokuWiki 2016-06-26a及之前的版本中的/inc/HTTPClient.php文件中的HTTPClient Class中的‘sendRequest’方法存在跨站请求伪造漏洞，该漏洞源于程序未能限制对专用网络的访问。攻击者可通过SSRF利用该漏洞扫描内部网络端口，例如：10.0.0.1/8，172.16.0.0/12，192.168.0.0/16。

Freefloat FTP Server是瑞典Freefloat公司的一套免费的用于上传文件和管理有线及无线设备的软件。
FreeFloat FTP Server 1.0版本中存在缓冲区溢出漏洞。远程攻击者可借助RMD命令中的长字符串利用该漏洞执行任意代码。
```

2. **【重要】**产品简介必须单独写一段，禁止使用夸张的语言描述漏洞简介。

正例：

```
DokuWiki是德国软件开发者 Andreas Gohr 所研发的一款基于 PHP 的 Wiki 引擎，它主要用于中小团队和个人网站知识库的管理，并提供版本控制、全文检索和权限控制等功能。
Freefloat FTP Server是瑞典Freefloat公司的一套免费的用于上传文件和管理有线及无线设备的软件。
```

反例：

```
海洋CMS又名SEACMS，完全开源免费，自适应电脑、手机、平板、APP多终端，无加密、更安全，是您最佳的建站工具!
ThinkCMF是一款支持Swoole的开源内容管理框架(CMF)，基于ThinkPHP开发,我们一直秉承ThinkPHP大道至简的理念，坚持做最简约的ThinkPHP开源软件,多应用化开发方式,让您更快地完成自己的创业项目！
```

## 漏洞分类

1. **【重要】**漏洞分类必须根据漏洞实际类型进行选择。

## Rank

1. **【重要】** Rank 值最高为5分。
2. **【重要】**Rank 必须根据漏洞实际类型以及漏洞利用复杂度评判。漏洞类型最高占比3分，漏洞复杂度占2分。详细规则如下：

漏洞分类：

| 漏洞类型   | 分值 |
| ---------- | ---- |
| 命令执行   | 1.0  |
| 代码执行   | 1.0  |
| 文件写入   | 1.5  |
| 文件上传   | 1.5  |
| 后门       | 1.5  |
| 默认口令   | 2.0  |
| 弱口令     | 2.0  |
| 权限绕过   | 2.5  |
| 未授权访问 | 1.5  |
| XXE 漏洞   | 3.0  |
| SQL 注入   | 3.0  |
| 文件读取   | 1.0  |
| 文件下载   | 1.0  |
| 文件包含   | 1.0  |
| 目录遍历   | 1.0  |

漏洞复杂度：

| 复杂度 | 权限要求 | 用户交互 | 分值 |
| ------ | -------- | -------- | ---- |
| 低     | 无       | 不需要   | 1.0  |
| 中     | 无       | 需要     | 1.5  |
| 高     | 有       | 需要     | 2.0  |

