package controller

import (
	"github.com/codinl/go-logger"
	"github.com/gin-gonic/gin"

	"wa_server/lib/status"
	"wa_server/lib/utils"
	"wa_server/model"

	"strconv"
	"fmt"
)

func QunPostChannelList(c *gin.Context) {
	type ChannelList struct {
		Main model.QunPostName   `json:"primary_channel"`
		List []model.QunPostName `json:"list"`
	}

	//获取主频道个数
	count, _ := model.PrimaryChannelCount()
	var data []ChannelList
	for i := 1; i <= count; i++ {
		primaryChannel, secondaryChannel := model.QunChannelList(uint32(i))
		result := ChannelList{
			List: secondaryChannel,
			Main: primaryChannel,
		}
		data = append(data, result)
	}

	RespJson(c, status.OK, data)
}

func QunPostList(c *gin.Context) {
	req := struct {
		Offset  uint32 `json:"offset"`
		Limit   uint32 `json:"limit"`
		Channel uint32 `json:"channel"` // 文章类型
	}{}
	if err := c.BindJSON(&req); err != nil {
		logger.Error(err)
		RespJson(c, status.BadRequest, nil)
		return
	}

	//u := auth.GetCurrentUser(c)
	//if u == nil {
	//	RespJson(c, status.Unauthorized, nil)
	//	return
	//}
	dbName := "qun_post_collection"
	posts, code := model.QunPostList(dbName, req.Offset, req.Limit, req.Channel)
	if code != status.OK {
		RespJson(c, code, nil)
		return
	}

	type Post struct {
		PostId   uint32 `json:"post_id" bson:"post_id"`
		AuthorId uint32 `json:"author_id" bson:"author_id"` // 作者ID
		Title    string `json:"title" bson:"title"`
		Channel  uint32 `json:"channel" bson:"channel"`     // 频道
		ShortUrl string `json:"short_url" bson:"short_url"` // 短网址
		Url      string `json:"url" bson:"url"`
		Content  string `json:"content" bson:"content"`
		Author   string `json:"author" bson:"author"`
	}
	var data []*Post
	for _, v := range posts {
		url := "https://wale.user.wawazhuawawa.com/woaiwoqun/index.html?post_id=" + strconv.Itoa(int(v.PostId))
		url = url+"%26channel="+strconv.Itoa(int(v.Channel))
		fmt.Print(url)
		ShortUrl, _ := utils.GetShortUrl(url)
		fmt.Print(url)
		post := &Post{
			PostId:   v.PostId,
			Title:    v.Title,
			AuthorId: v.AuthorId,
			Channel:  v.Channel,
			ShortUrl: ShortUrl,
			Url:      url,
			Content:  v.Content,
			Author:   v.Author,
		}
		data = append(data, post)
	}

	result := struct {
		Post []*Post `json:"post"`
	}{
		Post: data,
	}
	RespJson(c, status.OK, result)
}

// 获取文章详情
func QunPostGet(c *gin.Context) {
	req := struct {
		PostId uint32 `json:"post_id"` // 文章ID
	}{}
	if err := c.BindJSON(&req); err != nil {
		logger.Error(err)
		RespJson(c, status.BadRequest, nil)
		return
	}

	if req.PostId == 0 {
		RespJson(c, status.BadRequest, nil)
		return
	}

	post, code := model.QunPostGet(req.PostId)
	if code != status.OK {
		RespJson(c, code, nil)
		return
	}
	RespJsonEscapeHTML(c, status.OK, post)
}

func RecommendPostList(c *gin.Context) {
	req := struct {
		Offset  uint32 `json:"offset"`
		Limit   uint32 `json:"limit"`
		Channel uint32 `json:"channel"` // 文章类型
	}{}
	if err := c.BindJSON(&req); err != nil {
		logger.Error(err)
		RespJson(c, status.BadRequest, nil)
		return
	}

	//u := auth.GetCurrentUser(c)
	//if u == nil {
	//	RespJson(c, status.Unauthorized, nil)
	//	return
	//}
	dbName := "qun_post"
	posts, code := model.RecommendPostList(dbName, req.Offset, req.Limit, req.Channel)
	if code != status.OK {
		RespJson(c, code, nil)
		return
	}

	type Post struct {
		PostId   uint32 `json:"post_id" bson:"post_id"`
		Title    string `json:"title" bson:"title"`
		Channel  uint32 `json:"channel" bson:"channel"`     // 频道
		ShortUrl string `json:"short_url" bson:"short_url"` // 短网址
		Url      string `json:"url" bson:"url"`
		ImgUrl   string `json:"img_url" bson:"img_url"`
	}
	var data []*Post
	for _, v := range posts {

		if len(v.ImgUrl) != 0 {
			url := "https://wale.user.wawazhuawawa.com/woaiwoqun/index.html?post_id=" + strconv.Itoa(int(v.PostId))
			url = url+"&channel="+strconv.Itoa(int(v.Channel))
			ShortUrl, _ := utils.GetShortUrl(url)
			post := &Post{
				PostId:   v.PostId,
				Title:    v.Title,
				Channel:  v.Channel,
				ShortUrl: ShortUrl,
				Url:      url,
				ImgUrl:   v.ImgUrl[0],
			}

			data = append(data, post)
		}

	}

	result := struct {
		Post []*Post `json:"post"`
	}{
		Post: data,
	}
	RespJson(c, status.OK, result)
}
