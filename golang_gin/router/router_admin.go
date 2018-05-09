package router

import (
	"github.com/gin-gonic/gin"
	"wa_server/auth"
	"wa_server/controller"
)

func ConfigAdminRouter(r gin.IRouter) {
	//后台接口
	r.Use(CORSMiddleware())

	admin := r.Group("/admin")
	admin.POST("/login", controller.AdminLogin) //管理员登录

	adminAuth := admin.Use(auth.AdminAuth)
	{
		adminAuth.POST("/user/list", controller.UserList) //用户列表

		// TODO
		//adminAuth.POST("/key/config", controller.GetKeyConfigs)          // 获取口令配置
		//adminAuth.POST("/key/config/add", controller.AddKeyConfig)       // 添加口令配置
		//adminAuth.POST("/key/config/update", controller.UpdateKeyConfig) // 更新口令配置
		//adminAuth.POST("/key/config/check", controller.CheckKeyConfig)   // 验证配置

		// TODO 文章频道管理
		adminAuth.POST("/post/channel/list", controller.GetKeyConfigs)   // 频道列表
		adminAuth.POST("/post/channel/add", controller.GetKeyConfigs)    // 添加频道
		adminAuth.POST("/post/channel/delete", controller.GetKeyConfigs) // 删除频道
		adminAuth.POST("/post/channel/update", controller.GetKeyConfigs) // 更新频道

		// TODO 文章预览、编辑、审核
		//adminAuth.POST("/post/list/by_channel", controller.GetKeyConfigs) // 文章列表，按频道
		//adminAuth.POST("/post/get", controller.GetKeyConfigs)             // 文章详情
		//adminAuth.POST("/post/update", controller.GetKeyConfigs)          // 编辑文章
		//adminAuth.POST("/post/delete", controller.GetKeyConfigs)          // 删除文章
		//adminAuth.POST("/post/state/update", controller.GetKeyConfigs)    // 文章状态（上下架）管理

		// TODO
		admin.POST("/post/list", controller.AdminPostList)
		admin.POST("/post/delete", controller.AdminPostDelete)
		//admin.POST("/post/count", controller.AdminPostCount)
		admin.POST("/post/add", controller.AdminPostAdd)
		admin.POST("/post/update", controller.AdminPostUpdate)
		admin.POST("/post/state", controller.AdminPostUpdateState)

		adminAuth.POST("/wabao/product/add", controller.AdminWabaoProductAdd)
		adminAuth.POST("/wabao/product/list", controller.AdminWabaoProductList)
		adminAuth.POST("/wabao/product/delete", controller.AdminWabaoProductDelete)
		adminAuth.POST("/wabao/product/update", controller.AdminWabaoProductUpdate)
		adminAuth.POST("/wabao/product/shelf", controller.AdminWabaoProductShelf)

		adminAuth.POST("/wabao/issue/list", controller.AdminWabaoIssueList)

		admin.POST("/qun/list", controller.AdminQunList)
		admin.POST("/qun/post/list", controller.AdminQunPostList)
		admin.POST("/qun/post/collection", controller.QunCollectionPost)
		admin.POST("/qun/post/publish/list", controller.AdminCollectionList)
		admin.POST("/qun/post/history/list", controller.AdminHistoryList)
		admin.POST("/qun/post/delete", controller.AdminDeleteQunPost)
		admin.POST("/channel/list", controller.QunPostChannelList)



		adminAuth.POST("/version/add", controller.AddVersion) // 发布版本
	}

}
