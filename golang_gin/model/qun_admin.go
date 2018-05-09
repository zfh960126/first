package model

import (
	"github.com/codinl/go-logger"
	"gopkg.in/mgo.v2/bson"

	"wa_server/config"
	//"wa_server/lib/status"

	"fmt"
	"time"
)

//
//const URL = "localhost:27017"
//
//var (
//	mgoSession *mgo.Session
//)
//
//func getSession() *mgo.Session {
//	if mgoSession == nil {
//		var err error
//		mgoSession, err = mgo.Dial(URL)
//		if err != nil {
//			panic(err) //直接终止程序运行
//		}
//	}
//	//最大连接池默认为4096
//	return mgoSession.Clone()
//}

// 各频道统计
type AdminQunList struct {
	Id bson.ObjectId `json:"-" bson:"_id"`

	Channel     uint32    `json:"channel" bson:"channel"` // 频道
	PostType    uint32    `json:"post_type" bson:"post_type"`
	PublishDate time.Time `json:"publish_date" bson:"publish_date"`
	SelectCount uint32    `json:"select_count" bson:"select_count"` //人工选择的数量
	RandomCount uint32    `json:"random_count" bson:"random_count"` //系统随机选择的数量
	ReadCount   uint32    `json:"read_count" bson:"read_count"`     // 阅读数
	ShareCount  uint32    `json:"share_count" bson:"share_count"`   // 分享数量
	CopyCount   uint32    `json:"copy_count" bson:"copy_count"`     // 复制数量
}

type AdminQunPost struct {
	PostId    uint32    `json:"post_id" bson:"post_id"`
	TimeGap   string    `json:"time_gap" bson:"time_gap"`
	Source    string    `json:"source" bson:"source"`
	PublishAt time.Time `json:"publish_at" bson:"publish_at"`
	CreatedAt time.Time `json:"created_at" bson:"created_at"`
	//DeletedAt time.Time `json:"deleted_at" bson:"deleted_at"`
	Content     string    `json:"content" bson:"content"`
	Channel     uint32    `json:"channel" bson:"channel"`
	Title       string    `json:"title" bson:"title"`
	Author      string    `json:"author" bson:"author"`
	AuthorImg   string    `json:"author_img" bson:"author_img"`
	ImgUrl      []string  `json:"img_url" bson:"img_url"`
	Collection  int       `json:"collection" bson:"collection"`
	PublishDate time.Time `json:"publish_date" bson:"publish_date"`
}

//获取qun_main
func AdminQunMain(offset, limit int, doneAt, finishedAt time.Time, channel uint32) (posts []AdminQunList, count int, err error) {
	session := GetMongo().Clone()
	defer session.Close()
	c := session.DB(config.AppConfig.MgoDbName).C("qun_main")

	//session := getSession()
	//c := session.DB("qun_post").C("qun_main")

	query := bson.M{"publish_date": bson.M{"$lte": finishedAt, "$gte": doneAt}}
	if channel != 0 {
		query["channel"] = channel
	}

	er := c.Find(query).Sort("-publish_date").Skip(int(offset)).Limit(int(limit)).All(&posts)
	if er != nil {
		logger.Error(er)
		fmt.Print(er)
		return
	}

	count, erro := c.Find(query).Count()
	if erro != nil {
		logger.Error(erro)
		fmt.Print(erro)
		return
	}
	return
}

//文章列表
func AdminQunPostList(offset, limit, collection int, channel uint32, doneAt, finishedAt time.Time, title, dateType, dbName string) (posts []AdminQunPost, count int) {
	if limit == 0 {
		limit = 10
	}
	query := bson.M{dateType: bson.M{"$lte": finishedAt, "$gte": doneAt}}
	if title != "" {
		query["title"] = bson.M{"$regex": bson.RegEx{title, "."}}
	}
	if channel != 0 {
		query["channel"] = channel
	}

	query["collection"] = collection
	query["deleted_at"] = bson.M{"$exists": false}
	session := GetMongo().Clone()
	defer session.Close()
	c := session.DB(config.AppConfig.MgoDbName).C(dbName)

	//session := getSession()
	//c := session.DB("qun_post").C(dbName)
	er := c.Find(query).Sort("-post_id").Sort("-publish_at").Skip(int(offset)).Limit(int(limit)).All(&posts)
	if er != nil {
		fmt.Print(er)
		logger.Error(er)
		return nil, 0
	}

	count, err := c.Find(query).Count()
	if err != nil {
		fmt.Print(err)
		logger.Error(err)
		return nil, 0
	}
	return posts, count
}

func DeleteQunPost(postId uint32, dbName string) {
	session := GetMongo().Clone()
	defer session.Close()
	c := session.DB(config.AppConfig.MgoDbName).C(dbName)

	//session := getSession()
	//c := session.DB("qun_post").C(dbName)

	selector := bson.M{"post_id": postId}
	data := bson.M{"$set": bson.M{"deleted_at": time.Now().Local()}}
	er := c.Update(selector, data)
	if er != nil {
		fmt.Print(er)
		logger.Error(er)
		return
	}
	return
}

//采集
func CollectionQunPost(postId uint32, dbName string) {
	session := GetMongo().Clone()
	defer session.Close()
	c := session.DB(config.AppConfig.MgoDbName).C("qun_post")

	//session := getSession()
	//c := session.DB("qun_post").C("qun_post")

	post := AdminQunPost{}
	err := c.Find(bson.M{"post_id": postId}).One(&post)
	local, _ := time.LoadLocation("Local")
	post.CreatedAt, _ = time.ParseInLocation("2006-01-02 15:04:05Z", time.Now().Format("2006-01-02")+" 00:00:00Z", local)
	post.PublishDate, _ = time.ParseInLocation("2006-01-02 15:04:05Z", time.Now().Add(time.Hour*24).Format("2006-01-02")+" 00:00:00Z", local)

	if err != nil {
		fmt.Print(err)
		logger.Error(err)
		return
	}

	c2 := session.DB(config.AppConfig.MgoDbName).C(dbName)
	er := c2.Insert(&post)
	if er != nil {
		fmt.Print(er)
		logger.Error(er)
		return
	}
	return
}

//获取群的频道
func GetQunChannel() (channel []QunPostName) {
	session := GetMongo().Clone()
	defer session.Close()
	c := session.DB(config.AppConfig.MgoDbName).C("channel")
	//session := getSession()
	//c := session.DB("qun_post").C("channel")

	var primChannel []QunPostName
	query := bson.M{"channel": bson.M{"$gt": 0}}
	query["level"] = 1
	er := c.Find(query).All(&primChannel)

	if er != nil {
		logger.Error(er)
		fmt.Print(er)
		return
	}

	err := c.Find(bson.M{"level": 2}).All(&channel)
	if err != nil {
		logger.Error(err)
		fmt.Print(err)
		return
	}
	channel = append(channel, primChannel...)

	return
}

//获取post中某天数据
func AdminQunMainList(doneAt, finishedAt time.Time, channel int) (post []AdminQunList, count int, err error) {
	session := GetMongo().Clone()
	defer session.Close()
	c := session.DB(config.AppConfig.MgoDbName).C("qun_post_collection")
	//session := getSession()
	//c := session.DB("qun_post").C("qun_post_collection")

	query := bson.M{"publish_date": bson.M{"$lte": finishedAt, "$gte": doneAt}}
	query["channel"] = channel
	query["deleted_at"] = bson.M{"$exists": false}

	errs := c.Find(query).All(&post)
	if errs != nil {
		logger.Error(errs)
		fmt.Print(errs)
		return
	}

	count, er := c.Find(query).Count()
	if er != nil {
		logger.Error(er)
		fmt.Print(er)
		return
	}
	return
}

//更新qun_main
func UpdateMainList(publishDate time.Time, SelectCount, channel int, postType, readCount, shareCount, copyCount uint32) error {
	session := GetMongo().Clone()
	defer session.Close()
	c := session.DB(config.AppConfig.MgoDbName).C("qun_main")
	//session := getSession()
	//c := session.DB("qun_post").C("qun_main")

	//c.Insert(bson.M{"publish_date": publishDate,"channel": channel})

	selector := bson.M{"publish_date": publishDate, "channel": channel}
	data := bson.M{"$set": bson.M{"select_count": SelectCount, "publish_date": publishDate, "postType": postType, "readCount": readCount, "shareCount": shareCount, "copyCount": copyCount}}
	changeInfo, er := c.Upsert(selector, data)
	fmt.Print(changeInfo)
	return er
}
