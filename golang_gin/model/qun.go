package model

import (
	"gopkg.in/mgo.v2/bson"

	"wa_server/config"
	"wa_server/lib/status"

	"time"
)

// 文章
type QunPost struct {
	Id bson.ObjectId `json:"-" bson:"_id"`

	PostId   uint32 `json:"post_id" bson:"post_id"`
	AuthorId uint32 `json:"author_id" bson:"author_id"` // 作者ID
	Title    string `json:"title" bson:"title"`
	Content  string `json:"content" bson:"content"`
	Channel  uint32 `json:"channel" bson:"channel"`     // 频道
	ShortUrl string `json:"short_url" bson:"short_url"` // 短网址
	Url      string `json:"url" bson:"url"`
	Author   string `json:"author" bson:"author"`

	CreatedAt time.Time `json:"created_at" bson:"created_at"`
	DeletedAt time.Time `json:"deleted_at" bson:"deleted_at"`

	ReadCount  uint32   `json:"read_count" bson:"read_count"`   // 阅读数
	ShareCount uint32   `json:"share_count" bson:"share_count"` // 分享数量
	TimeGap    string   `json:"time_gap" bson:"time_gap"`
	Source     string   `json:"source" bson:"source"`
	ImgUrl     []string `json:"img_url" bson:"img_url"`

	State uint32 `json:"state" bson:"state"`
}

// 群 频道
type QunChannel struct {
	//Model
	Name     string `json:"name"`
	ParentId uint32 `json:"parent_id"` // 上一层级的ID
	Level    uint32 `json:"level"`     // 层级 1- 2-
	IndexNum uint32 `json:"index_num"` // 优先序列号
	State    uint32 `json:"state"`
}

type QunPostName struct {
	Name    string `json:"name"`
	Channel uint32    `json:"channel"`
}

//获取主频道个数
func PrimaryChannelCount() (count int, err error) {
	session := GetMongo().Clone()
	defer session.Close()
	c := session.DB(config.AppConfig.MgoDbName).C("channel")
	//session := getSession()
	//c := session.DB("qun_post").C("channel")

	count, er := c.Find(bson.M{"state": 1, "level": 1}).Count()
	if er != nil {
		return
	}
	return
}

func QunChannelList(parentId uint32) (primaryChannel QunPostName, SecondaryChannel []QunPostName) {
	session := GetMongo().Clone()
	defer session.Close()
	c := session.DB(config.AppConfig.MgoDbName).C("channel")

	//session := getSession()
	//c := session.DB("qun_post").C("channel")

	primaryChannel = QunPostName{}
	er := c.Find(bson.M{
		"parent_id": parentId, "state": 1, "level": 1}).One(&primaryChannel)
	if er != nil {
		return
	}
	err := c.Find(bson.M{
		"parent_id": parentId, "state": 1, "level": 2}).All(&SecondaryChannel)
	if err != nil {
		return
	}
	return primaryChannel, SecondaryChannel
}

func QunPostList(dbName string, offset, limit, channel uint32) (post []QunPost, code int) {
	if limit == 0 {
		limit = 10
	}

	session := GetMongo().Clone()
	defer session.Close()
	c := session.DB(config.AppConfig.MgoDbName).C(dbName)
	//session := getSession()
	//c := session.DB("qun_post").C("qun_post_collection")

	//local, _ := time.LoadLocation("Local")
	//doneAt, _ := time.ParseInLocation("2006-01-02 15:04:05Z", time.Now().Format("2006-01-02")+" 00:00:00Z", local)
	//finishedAt, _ := time.ParseInLocation("2006-01-02 15:04:05Z", time.Now().Add(time.Hour*24).Format("2006-01-02")+" 00:00:00Z", local)
	//
	//query := bson.M{"publish_at": bson.M{"$lte": finishedAt, "$gte": doneAt}}

	//local, _ := time.LoadLocation("Local")
	//doneAt, _ := time.ParseInLocation("2006-01-02 15:04:05Z", time.Now().Format("2006-01-02")+" 00:00:00Z", local)
	//finishedAt, _ := time.ParseInLocation("2006-01-02 15:04:05Z", time.Now().Add(time.Hour*24).Format("2006-01-02")+" 00:00:00Z", local)
	//
	//query := bson.M{"publish_date": bson.M{"$lte": finishedAt, "$gte": doneAt}}
	//
	//query["channel"] = channel
	//query["deleted_at"] = bson.M{"$exists": false}

	query := bson.M{"channel": channel, "deleted_at": bson.M{"$exists": false}}
	err := c.Find(query).Sort("-created_at").Skip(int(offset)).Limit(int(limit)).All(&post)
	if err != nil {
		return nil, status.DBOperateError
	}

	return post, status.OK
}

func RecommendPostList(dbName string, offset, limit, channel uint32) (post []QunPost, code int) {
	if limit == 0 {
		limit = 10
	}

	session := GetMongo().Clone()
	defer session.Close()
	c := session.DB(config.AppConfig.MgoDbName).C(dbName)

	err := c.Find(bson.M{
		"channel": channel, "deleted_at": bson.M{"$exists": false}}).Sort("-created_at").Skip(int(offset)).Limit(int(limit)).All(&post)
	if err != nil {
		return nil, status.DBOperateError
	}

	return post, status.OK
}

func QunPostGet(postId uint32) (*QunPost, int) {
	session := GetMongo().Clone()
	defer session.Close()
	c := session.DB(config.AppConfig.MgoDbName).C("qun_post")
	//session := getSession()
	//c := session.DB("qun_post").C("qun_post_collection")

	post := &QunPost{}
	err := c.Find(bson.M{
		"post_id": postId}).One(&post)
	if err != nil {
		return nil, status.DBOperateError
	}

	return post, status.OK
}
