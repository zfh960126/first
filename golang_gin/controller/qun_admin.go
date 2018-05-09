package controller

import (
	"github.com/codinl/go-logger"
	"github.com/gin-gonic/gin"

	"wa_server/lib/status"
	"wa_server/model"

	"fmt"
	"time"
)

type QunPost struct {
	PostId      uint32    `json:"post_id" bson:"post_id"`
	Title       string    `json:"title" bson:"title"`
	Content     string    `json:"content" bson:"content"`
	Channel     uint32    `json:"channel" bson:"channel"` // 频道
	Url         string    `json:"url" bson:"url"`
	CreatedAt   time.Time `json:"created_at" bson:"created_at"`
	PublishAt   time.Time `json:"publish_at" bson:"publish_at"`
	ReadCount   uint32    `json:"read_count" bson:"read_count"`   // 阅读数
	ShareCount  uint32    `json:"share_count" bson:"share_count"` // 分享数量
	TimeGap     string    `json:"time_gap" bson:"time_gap"`
	Source      string    `json:"source" bson:"source"`
	Author      string    `json:"author" bson:"author"`
	ImgUrl      []string  `json:"img_url" bson:"img_url"`
	State       uint32    `json:"state" bson:"state"`
	PublishDate time.Time `json:"publish_date" bson:"publish_date"`
}

type PostResult struct {
	Post  []*QunPost `json:"post"`
	Count int        `json:"count"`
}

func GetQunPostList(offset, limit, collection int, channel uint32, doneAt, finishedAt, title, dateType, dbName string) PostResult {
	local, _ := time.LoadLocation("Local")
	var DoneAt time.Time
	var FinishedAt time.Time

	if doneAt == "" {
		t1, _ := time.ParseInLocation("2006-01-02T15:04:05Z", "2001-01-02T15:04:05Z", local)
		DoneAt = t1
	} else {
		t1, _ := time.ParseInLocation("2006-01-02 15:04:05", doneAt, local)
		DoneAt = t1
	}
	if finishedAt == "" {
		t2, _ := time.ParseInLocation("2006-01-02T15:04:05Z", "2030-01-02T15:04:05Z", local)
		FinishedAt = t2
	} else {
		t2, _ := time.ParseInLocation("2006-01-02 15:04:05", finishedAt, local)
		FinishedAt = t2
	}
	//u := auth.GetCurrentUser(c)
	//if u == nil {
	//	RespJson(c, status.Unauthorized, nil)
	//	return
	//}
	posts, count := model.AdminQunPostList(offset, limit, collection, channel, DoneAt, FinishedAt, title, dateType, dbName)
	var datas []*QunPost
	for _, v := range posts {
		post := &QunPost{
			PostId:      v.PostId,
			Title:       v.Title,
			Channel:     v.Channel,
			Author:      v.Author,
			Source:      v.Source,
			PublishAt:   v.PublishAt,
			CreatedAt:   v.CreatedAt,
			Content:     v.Content,
			TimeGap:     v.TimeGap,
			ImgUrl:      v.ImgUrl,
			PublishDate: v.PublishDate,
		}
		datas = append(datas, post)
	}

	results := PostResult{
		Post:  datas,
		Count: count,
	}
	return results
}

//查看发布文章历史
func AdminHistoryList(c *gin.Context) {
	req := struct {
		Offset     int    `json:"offset"`
		Limit      int    `json:"limit"`
		Channel    uint32 `json:"channel"`
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

	dateType := "publish_at"
	dbName := "qun_post_history"
	Collection := 1
	result := GetQunPostList(req.Offset, req.Limit, Collection, req.Channel, req.DoneAt, req.FinishedAt, req.Title, dateType, dbName)
	//u := auth.GetCurrentUser(c)
	//if u == nil {
	//	RespJson(c, status.Unauthorized, nil)
	//	return
	//}
	RespJson(c, status.OK, result)
}

//文章列表
func AdminQunPostList(c *gin.Context) {
	req := struct {
		Offset     int    `json:"offset"`
		Limit      int    `json:"limit"`
		Channel    uint32 `json:"channel"`
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

	dateType := "publish_at"
	dbName := "qun_post"
	Collection := 1
	result := GetQunPostList(req.Offset, req.Limit, Collection, req.Channel, req.DoneAt, req.FinishedAt, req.Title, dateType, dbName)
	//u := auth.GetCurrentUser(c)
	//if u == nil {
	//	RespJson(c, status.Unauthorized, nil)
	//	return
	//}
	RespJson(c, status.OK, result)
}

//当前发布的文章
func AdminCollectionList(c *gin.Context) {
	req := struct {
		Offset     int    `json:"offset"`
		Limit      int    `json:"limit"`
		Channel    uint32 `json:"channel"`
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

	dateType := "publish_at"
	dbName := "qun_post_collection"
	Collection := 1
	result := GetQunPostList(req.Offset, req.Limit, Collection, req.Channel, req.DoneAt, req.FinishedAt, req.Title, dateType, dbName)
	//u := auth.GetCurrentUser(c)
	//if u == nil {
	//	RespJson(c, status.Unauthorized, nil)
	//	return
	//}
	RespJson(c, status.OK, result)
}

//采集
func QunCollectionPost(c *gin.Context) {
	req := struct {
		PostId []uint32 `json:"post_id"`
	}{}
	if err := c.BindJSON(&req); err != nil {
		logger.Error(err)
		RespJson(c, status.BadRequest, nil)
		return
	}

	for _, PostId := range req.PostId {
		model.CollectionQunPost(PostId, "qun_post_collection")
		model.CollectionQunPost(PostId, "qun_post_history")
		model.DeleteQunPost(PostId, "qun_post")
	}
	//u := auth.GetCurrentUser(c)
	//if u == nil {
	//	RespJson(c, status.Unauthorized, nil)
	//	return
	//}
	RespJson(c, status.OK, req.PostId)
}

//删除
func AdminDeleteQunPost(c *gin.Context) {
	req := struct {
		PostId uint32 `json:"post_id"`
		DbName string `json:"db_name"`
	}{}
	if err := c.BindJSON(&req); err != nil {
		logger.Error(err)
		RespJson(c, status.BadRequest, nil)
		return
	}
	model.DeleteQunPost(req.PostId, req.DbName)

	RespJson(c, status.OK, req.PostId)
}

func AdminQunList(c *gin.Context) {
	req := struct {
		Offset  int    `json:"offset"`
		Limit   int    `json:"limit"`
		Channel uint32 `json:"channel"`
		//State      int    `json:"state"`
		//Title      string `json:"title"`
		DoneAt     string `json:"done_at"`
		FinishedAt string `json:"finished_at"`
		//Source     string `json:"source"`
	}{}
	if err := c.BindJSON(&req); err != nil {
		logger.Error(err)
		RespJson(c, status.BadRequest, nil)
		return
	}

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

	t1, _ := time.ParseInLocation("2006-01-02 15:04:05Z", time.Now().Format("2006-01-02")+" 00:00:00Z", local)
	t2, _ := time.ParseInLocation("2006-01-02 15:04:05Z", time.Now().Add(time.Hour*24).Format("2006-01-02")+" 00:00:00Z", local)
	CountQunCollection(t1, t2)

	posts, count, _ := model.AdminQunMain(req.Offset, req.Limit, DoneAt, FinishedAt, req.Channel)
	var datas []*model.AdminQunList
	for _, v := range posts {
		post := &model.AdminQunList{
			Channel:     v.Channel,
			PostType:    v.PostType,
			PublishDate: v.PublishDate,
			SelectCount: v.SelectCount,
			ReadCount:   v.ReadCount,
			ShareCount:  v.ShareCount,
			CopyCount:   v.CopyCount,
		}
		datas = append(datas, post)
	}
	results := struct {
		Post  []*model.AdminQunList `json:"post"`
		Count int                   `json:"count"`
	}{
		Post:  datas,
		Count: count,
	}
	RespJson(c, status.OK, results)
}

//统计发布数据
func CountQunCollection(doneAt, finishedAt time.Time) {
	qunPostNames := model.GetQunChannel()

	for _, qunPostName := range qunPostNames {
		posts, SelectCount, err := model.AdminQunMainList(doneAt, finishedAt, int(qunPostName.Channel))
		var postType, readCount, shareCount, copyCount uint32
		if err != nil {
			return
		}

		for _, post := range posts {
			readCount = readCount + post.ReadCount
			shareCount = shareCount + post.ShareCount
			copyCount = copyCount + post.CopyCount
			postType = post.PostType
		}
		er := model.UpdateMainList(doneAt, SelectCount, int(qunPostName.Channel), postType, readCount, shareCount, copyCount)
		if er != nil {
			logger.Error(er)
			fmt.Print(er)
			return
		}
	}
	return
}

//转换url
//func AdminDeleteQunPost(c *gin.Context) {
//	req := struct {
//		PostId uint32 `json:"post_id"`
//		DbName string `json:"db_name"`
//	}{}
//	if err := c.BindJSON(&req); err != nil {
//		logger.Error(err)
//		RespJson(c, status.BadRequest, nil)
//		return
//	}
//
//	//for _, PostId := range req.PostId {
//	model.DeleteQunPost(req.PostId, req.DbName)
//
//	//}
//	//u := auth.GetCurrentUser(c)
//	//if u == nil {
//	//	RespJson(c, status.Unauthorized, nil)
//	//	return
//	//}
//	RespJson(c, status.OK, req.PostId)
//}
