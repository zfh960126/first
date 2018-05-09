package model

import (
	"github.com/codinl/go-logger"
	_ "gopkg.in/mgo.v2"
	"gopkg.in/mgo.v2/bson"

	"fmt"
	"time"

	"wa_server/config"
)

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
type PostAdmin struct {
	ID           bson.ObjectId `json:"-" bson:"_id"`
	PostId       uint32        `json:"post_id" bson:"post_id"`
	Title        string        `json:"title" bson:"title"`
	Content      string        `json:"content" bson:"content"`
	Source       string        `json:"source" bson:"source"`
	Channel      uint32        `json:"channel" bson:"channel"`
	ImgUrl       []string      `json:"img_url" bson:"img_url"`
	PublishAt    time.Time     `json:"publish_at" bson:"publish_at"`
	Author       string        `json:"author" bson:"author"`
	ImgCount     uint32        `json:"img_count" bson:"img_count"`
	CreatedAt    time.Time     `json:"created_at" bson:"created_at"`
	CommentCount uint32        `json:"comment_count" bson:"comment_count"`
	WordCount    uint32        `json:"word_count" bson:"word_count"` //文章字数
	ReadCount    uint32        `json:"read_count" bson:"read_count"`
	State        uint32        `json:"state" bson:"state"`
	AuthorImg    string        `json:"author_img" bson:"author_img"` //作者头像
	TimeGap      string        `json:"time_gap" bson:"time_gap"`
}

type PostID struct {
	PostId uint32 `json:"post_id" bson:"post_id"`
}

//
//type News
// Type struct {
//
//
//	Type string `json:"type"` // 类型
//}
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

func GetPostList(offset, limit, channel int, doneAt, finishedAt time.Time, title, source string) (posts []PostAdmin, count int) {
	if limit == 0 {
		limit = 10
	}
	query := bson.M{"publish_at": bson.M{"$lte": finishedAt, "$gte": doneAt}}

	if title != "" {
		//query["title"] = bson.M{"title": bson.M{"$regex": title, "$options": "s"}}
		query["title"] = bson.M{"$regex": bson.RegEx{title, "."}}
	}
	if source != "" {
		query["source"] = bson.M{"source": source}
	}
	if channel != 0 {
		query["channel"] = channel
	}

	session := GetMongo().Clone()
	//session := getSession()
	defer session.Close()
	c := session.DB(config.AppConfig.MgoDbName).C("post")
	//c := session.DB("网易新闻_app").C("wangyi")
	err := c.Find(query).Sort("-post_id").Sort("-publish_at").Skip(int(offset)).Limit(int(limit)).All(&posts)
	if err != nil {
		logger.Error(err)
		return nil, 0
	}

	count, err = c.Find(query).Count()
	if err != nil {
		logger.Error(err)
		return nil, 0
	}
	return posts, count
}

func DeletePost(PostId int) bool {
	session := GetMongo().Clone()
	//session := getSession()
	defer session.Close()
	c := session.DB(config.AppConfig.MgoDbName).C("post")
	//c := session.DB("网易新闻_app").C("wangyi")

	_, er := c.RemoveAll(bson.M{"post_id": PostId})
	if er != nil {
		fmt.Print(er)
		logger.Error(er)
		return true
	}
	return false
}

func Count() int {
	session := GetMongo().Clone()
	//session := getSession()
	defer session.Close()
	c := session.DB(config.AppConfig.MgoDbName).C("post")
	//c := session.DB("网易新闻_app").C("wangyi")
	countNum, _ := c.Count()
	return countNum
}

func UpdatePost(postId, channel, wordCount, imgCount int, title, content, publisher, authorImg string, imgUrl []string) (post []PostAdmin) {
	session := GetMongo().Clone()
	//session := getSession()
	defer session.Close()
	c := session.DB(config.AppConfig.MgoDbName).C("post")
	//c := session.DB("网易新闻_app").C("wangyi")

	selector := bson.M{"post_id": postId}
	data := bson.M{"$set": bson.M{"title": title, "content": content, "channel": channel, "img_url": imgUrl, "publisher": publisher, "img_count": imgCount,
		"created_at": time.Now().Local(), "author_img": authorImg, "word_count": wordCount,
	}}

	er := c.Update(selector, data)
	if er != nil {
		logger.Error(er)
		return nil
	}

	err := c.Find(bson.M{"post_id": postId}).All(&post)
	if err != nil {
		logger.Error(err)
		return nil
	}
	return post
}

func AddPost(channel, ImgCount, wordCount int, title, content, source, author, authorImg string, imgUrl []string) error {
	session := GetMongo().Clone()
	//session := getSession()
	defer session.Close()
	c := session.DB(config.AppConfig.MgoDbName).C("post")
	//c := session.DB("网易新闻_app").C("wangyi")
	//c2 := session.DB("Post").C("post_id")
	c2 := session.DB(config.AppConfig.MgoDbName).C("post_id")

	//mongo $inc id自增
	var AddId PostID
	err := c2.Find(bson.M{"id": "post_id"}).One(&AddId)
	if err != nil {
		logger.Error(err)
		return nil
	}
	postId := AddId.PostId + 1

	selector := bson.M{"id": "post_id"}
	data := bson.M{"$inc": bson.M{"post_id": 1}}
	erro := c2.Update(selector, data)
	if erro != nil {
		logger.Error(erro)
		return nil
	}

	url := ""
	source = "挖乐"
	state := 0

	er := c.Insert(bson.M{"post_id": postId, "channel": channel, "img_count": ImgCount, "title": title,
		"content": content, "source": source, "author": author, "publish_at": time.Now().Local(), "img_url": imgUrl,
		"created_at": time.Now().Local(), "url": url, "state": state, "word_count": wordCount, "author_img": authorImg})
	return er
}

func UpdateState(postId, state int) error {
	session := GetMongo().Clone()
	//session := getSession()
	defer session.Close()
	c := session.DB(config.AppConfig.MgoDbName).C("post")
	//c := session.DB("网易新闻_app").C("wangyi")

	selector := bson.M{"post_id": postId}
	data := bson.M{"$set": bson.M{"state": state}}

	er := c.Update(selector, data)
	return er
}
