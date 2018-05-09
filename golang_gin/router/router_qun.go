package router

import (
	"github.com/gin-gonic/gin"
	"wa_server/controller"
)

func ConfigQunRouter(r gin.IRouter) {

	r.Use(CORSMiddleware())

	api := r.Group("/api/" + API_VERSION + "/qun")
	{
	}

	//api.Use(auth.UserAuth)
	{
		api.POST("/channel/list", controller.QunPostChannelList)
		api.POST("/post/list", controller.QunPostList)
		api.POST("/qun/get", controller.QunPostGet)
		api.POST("/recommend", controller.RecommendPostList)
	}
}
