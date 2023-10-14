# ZZU-ClassRoom
郑州大学空教室查询，出于本人需求只做了北核的。

## 环境变量配置
需要在GitHub Secrets中添加以下变量
|   Repository Secrets   | Description |
| ----------- | ----------- |
| `EMAIL` | GitHub邮箱 |
| `USERNAME` | GitHub用户名 |
| `GH_ACCESS_TOKEN` | 有`repo`权限的 GitHub Access Token |
| `ZZU_CONFIG` | 用于配置`ZZU-API`，详情请看[ZZU-API](https://github.com/TorCroft/ZZU-API) |

`ZZU_CONFIG`内容如下，只填写 `Account` 和 `Password` 即可。
``` Json
{
    "Account": "",
    "Password": "",
    "UserToken": "",
    "Token": "",
    "JsessionId": "",
    "Tid": "",
    "RefreshToken": "",
    "ECardAccessToken": ""
}
```


## 说明
本项目使用了 [ZZU-API](https://github.com/TorCroft/ZZU-API)
