package controller

import (
	"github.com/codinl/go-logger"
	"github.com/gin-gonic/gin"

	"fmt"
	"time"

	_ "wa_server/auth"
	"wa_server/lib/status"
	"wa_server/model"
)

/**
* @api {post} admin/post/list
* @apiName list
* @apiGroup admin
* @apiPermission 需要登录
* @apiParam {int} Offset 	分页参数
* @apiParam {int} Limit  	分页参数
* @apiParam {int} Channel  	文章频道，1-24
* @apiParam {int} PostId 	文章ID
* @apiParam {int} State 	是否显示，0不显示，1显示
* @apiParam {string} Title  文章标题
* @apiParam {string} DoneAt  		搜索开始时间
* @apiParam {string}  FinishedAt	搜索结束时间
* @apiParam {string} Source			文章来源
*
* @apiSuccessExample {json} 成功返回
* {
*
* }
* @apiUse Error_default
 */
func AdminPostList(c *gin.Context) {
	req := struct {
		Offset     int    `json:"offset"`
		Limit      int    `json:"limit"`
		Channel    int    `json:"channel"`
		State      int    `json:"state"`
		Title      string `json:"title"`
		DoneAt     string `json:"done_at"`
		FinishedAt string `json:"finished_at"`
		Source     string `json:"source"`
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

	local, _ := time.LoadLocation("Local")
	var DoneAt time.Time
	var FinishedAt time.Time

	if req.DoneAt == "" {
		t1, _ := time.ParseInLocation("2006-01-02T15:04:05Z", "2001-01-02T15:04:05Z", local)
		DoneAt = t1
	} else {
		t1, _ := time.ParseInLocation("2006-01-02 15:04:05", req.DoneAt, local)
		DoneAt = t1
	}
	if req.FinishedAt == "" {
		t2, _ := time.ParseInLocation("2006-01-02T15:04:05Z", "2030-01-02T15:04:05Z", local)
		FinishedAt = t2
	} else {
		t2, _ := time.ParseInLocation("2006-01-02 15:04:05", req.FinishedAt, local)
		FinishedAt = t2
	}
	//u := auth.GetCurrentUser(c)
	//if u == nil {
	//	RespJson(c, status.Unauthorized, nil)
	//	return
	//}

	posts, count := model.GetPostList(req.Offset, req.Limit, req.Channel, DoneAt, FinishedAt, req.Title, req.Source)

	type Post struct {
		PostId       uint32    `json:"post_id" bson:"post_id"`
		Title        string    `json:"title" bson:"title"`
		Channel      uint32    `json:"channel" bson:"channel"`
		ImgUrl       []string  `json:"img_url" bson:"img_url"`
		CreatedAt    time.Time `json:"created_at" bson:"created_at"`
		Author       string    `json:"author" bson:"author"`
		ImgCount     uint32    `json:"img_count" bson:"img_count"`
		Source       string    `json:"source" bson:"source"`
		PublishAt    time.Time `json:"publish_at" bson:"publish_at"`
		CommentCount uint32    `json:"comment_count" bson:"comment_count"`
		WordCount    uint32    `json:"word_count" bson:"word_count"`
		ReadCount    uint32    `json:"read_count" bson:"read_count"`
		Content      string    `json:"content" bson:"content"`
		State        uint32    `json:"state" bson:"state"`
		AuthorImg    string    `json:"author_img" bson:"author_img"`
		TimeGap      string    `json:"time_gap" bson:"time_gap"`
	}
	var datas []*Post
	for _, v := range posts {
		post := &Post{
			PostId:       v.PostId,
			Title:        v.Title,
			Channel:      v.Channel,
			ImgUrl:       v.ImgUrl,
			CreatedAt:    v.CreatedAt,
			Author:       v.Author,
			ImgCount:     v.ImgCount,
			Source:       v.Source,
			PublishAt:    v.PublishAt,
			CommentCount: v.CommentCount,
			WordCount:    v.WordCount,
			ReadCount:    v.ReadCount,
			Content:      v.Content,
			State:        v.State,
			AuthorImg:    v.AuthorImg,
			TimeGap:      v.TimeGap,
		}
		datas = append(datas, post)
	}

	result := struct {
		Post  []*Post `json:"post"`
		Count int     `json:"count"`
	}{
		Post:  datas,
		Count: count,
	}
	RespJson(c, status.OK, result)
}

/**
* @api {post} admin/post/delete
* @apiName delete
* @apiGroup admin
* @apiPermission 需要登录
* @apiParam {int} PostId 文章ID
*
* @apiSuccessExample {json} 成功返回
* {
*	"code": 200,
	"desc": "成功",
	"data": "update successful [3219]"
* }
* @apiUse Error_default
*/
func AdminPostDelete(c *gin.Context) {
	req := struct {
		PostId []int `json:"post_id"`
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

	for _, PostId := range req.PostId {
		model.DeletePost(PostId)
	}
	msg := fmt.Sprintf("update successful %d", req.PostId)
	RespJson(c, status.OK, msg)
}

/**
* @api {post} admin/post/add
* @apiName add
* @apiGroup admin
* @apiPermission 需要登录
* @apiParam {int} Channel  			文章分类，1-24
* @apiParam {int} PostId 			文章ID
* @apiParam {string} Title  		文章标题
* @apiParam {string} Source			文章来源
* @apiParam {int} ImgUrlCount		文章类别
* @apiParam {string} Author			文章作者
* @apiParam {time.Time} CreatedAt	文章发布时间
* @apiParam {[]string} ImgUrl		文章图片url
* @apiParam {int} WordCount			文章字数
* @apiParam {string} Content		文章内容
*
* @apiSuccessExample {json} 成功返回
* {
*
* }
* @apiUse Error_default
 */
func AdminPostAdd(c *gin.Context) {
	req := struct {
		Channel   int       `json:"channel"`
		ImgCount  int       `json:"img_count"`
		Title     string    `json:"title"`
		Content   string    `json:"content"`
		Source    string    `json:"source"`
		Author    string    `json:"author"`
		CreatedAt time.Time `json:"created_at"`
		ImgUrl    []string  `json:"img_url"`
		WordCount int       `json:"word_count"`
		AuthorImg string    `json:"author_img"`
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

	if len(req.ImgUrl) >= 3 {
		req.ImgCount = 3
	}
	if len(req.ImgUrl) >= 1 && len(req.ImgUrl) < 3 {
		req.ImgCount = 1
	}
	if len(req.ImgUrl) == 0 {
		req.ImgCount = 0
	}

	er := model.AddPost(req.Channel, req.ImgCount, req.WordCount, req.Title, req.Content, req.Source, req.Author, req.AuthorImg, req.ImgUrl)
	if er != nil {
		logger.Error(er)
		RespJson(c, status.BadRequest, nil)
		return
	}
	msg := fmt.Sprintf("Add successful %d", req.Title)
	RespJson(c, status.OK, msg)
}

/**
* @api {post} admin/post/update
* @apiName update
* @apiGroup admin
* @apiPermission 需要登录
** @apiParam {int} Channel  	文章分类，1-24
* @apiParam {int} PostId 		文章ID
* @apiParam {string} Title  	文章标题
* @apiParam {int} ImgUrlCount	文章类别
* @apiParam {string} Author		文章作者
* @apiParam {[]string} ImgUrl	文章图片url
* @apiParam {int} WordCount		文章字数
* @apiParam {string} Content	文章内容
*
* @apiSuccessExample {json} 成功返回
* {
*
* }
* @apiUse Error_default
 */
func AdminPostUpdate(c *gin.Context) {
	req := struct {
		Channel   int      `json:"channel"`
		PostId    int      `json:"post_id"`
		ImgCount  int      `json:"img_count"`
		Title     string   `json:"title"`
		Content   string   `json:"content"`
		Author    string   `json:"author"`
		ImgUrl    []string `json:"img_url"`
		AuthorImg string   `json:"author_img"`
		WordCount int      `json:"word_count"`
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
	fmt.Print(req.PostId, req.Channel)
	if len(req.ImgUrl) >= 3 {
		req.ImgCount = 3
	}
	if len(req.ImgUrl) >= 1 && len(req.ImgUrl) < 3 {
		req.ImgCount = 1
	}
	if len(req.ImgUrl) == 0 {
		req.ImgCount = 0
	}

	posts := model.UpdatePost(req.PostId, req.Channel, req.WordCount, req.ImgCount, req.Title, req.Content, req.Author, req.AuthorImg, req.ImgUrl)
	RespJson(c, status.OK, posts)
}

/**
* @api {post} admin/post/state
* @apiName state
* @apiGroup admin
* @apiPermission 需要登录
* @apiParam {int} State 是否显示，0不显示，1显示
* @apiParam {int} PostId 文章ID
*
* @apiSuccessExample {json} 成功返回
* {
*
* }
* @apiUse Error_default
 */
func AdminPostUpdateState(c *gin.Context) {
	req := struct {
		State  int `json:"state"`
		PostId int `json:"post_id"`
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
	fmt.Print(req.PostId, req.State)
	er := model.UpdateState(req.PostId, req.State)
	if er != nil {
		logger.Error(er)
		RespJson(c, status.BadRequest, nil)
		return
	}
	msg := fmt.Sprintf("UpdateState successful %d", req.PostId)
	RespJson(c, status.OK, msg)
}
