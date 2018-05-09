package model

import (
	"github.com/codinl/go-logger"
	"gopkg.in/mgo.v2/bson"

	"wa_server/config"

	"fmt"
	"strconv"
	"time"
)

type WaProduct struct {
	ProductId int `json:"product_id" form:"product_id"`
	//Id        int    `json:"id" form:"id"`
	Name string `json:"name" form:"name"`
	//Descr string `json:"descr"` // 简介
	TotalCount int    `json:"total_count" form:"total_count"`
	Coin       int    `json:"coin" form:"coin"` // 每次金币
	State      int    `json:"state" form:"state"`
	MainImg    string `json:"main_img" form:"main_img"` // 主图
	CreatedAt  string `json:"created_at" form:"created_at"`
	UpdatedAt  string `json:"updated_at" form:"updated_at"`
	DeletedAt  string `json:"deleted_at" form:"deleted_at"`
	Price      int    `json:"price" form:"price"`
	Imgs       string `json:"imgs" form:"imgs"` // 轮播图
	DetailImg  string `json:"detail_img" form:"detail_img"`
	CurrentNo  int    `json:"current_no" form:"current_no"`
}

type WaIssue struct {
	ProductId   int    `json:"product_id" form:"product_id"`
	Id          int    `json:"id" form:"id"`
	Name        string `json:"name" form:"name"`
	TotalCount  int    `json:"total_count" form:"total_count"`
	Coin        uint32 `json:"coin"`
	CreatedAt   string `json:"created_at" form:"created_at"`
	SoldCount   int    `json:"sold_count" form:"sold_count"`
	AddPeople   int    `json:"add_people" form:"add_people"`
	State       int    `json:"state" form:"state"`
	LuckyNumber uint32 `json:"lucky_number"` // 中奖号码
	FinishedAt  string `json:"finished_at" form:"finished_at"`
	IssueNo     int    `json:"issue_no" form:"issue_no"`

	Uid          int    `json:"uid" bson:"uid" db:"uid"`                                            //用户ID
	UserName     string `json:"user_name" bson:"user_name" db:"user_name"`                          //用户名
	NickName     string `json:"nick_name" bson:"nick_name" db:"nick_name"`                          //昵称
	Tel          string `json:"tel" bson:"tel" db:"tel"`                                            //手机号
	WeixinUid    string `json:"weixin_uid" bson:"weixin_uid" gorm:"type:varchar(128);unique_index"` //微信UnionID
	WeixinOpenid string `json:"weixin_openid" bson:"weixin_openid"`                                 //微信openid
}

//type WaUser struct {
//	Id           uint32 `json:"id" bson:"_id,omissuepty" gorm:"primary_key"`
//	Uid          int    `json:"uid" bson:"uid" db:"uid" gorm:"index"`                               //用户ID
//	UserName     string `json:"user_name" bson:"user_name" db:"user_name"`                          //用户名
//	NickName     string `json:"nick_name" bson:"nick_name" db:"nick_name"`                          //昵称
//	Tel          int    `json:"tel" bson:"tel" db:"tel"`                                            //手机号
//	WeixinUid    string `json:"weixin_uid" bson:"weixin_uid" gorm:"type:varchar(128);unique_index"` //微信UnionID
//	WeixinOpenid string `json:"weixin_openid" bson:"weixin_openid"`                                 //微信openid
//}

func AdminAddProduct(currentNo,productId, totalCount, coin, state, price int, name, mainImg, createdAt, updatedAt, imgs, detailImg string) (id int64, err error) {
	//dbs, err := gorm.Open("mysql", "root:123456@tcp(127.0.0.1:3306)/wabao_development")
	_ = db.Exec(`INSERT INTO wabao_product(current_no,id,name,total_count,coin,state,main_img,created_at,
    	updated_at,price,imgs,detail_img) VALUES ( ?,?, ?, ?, ?,?, ?, ?, ?, ?, ?)`,currentNo, productId, name, totalCount, coin, state, mainImg, createdAt, updatedAt, price, imgs, detailImg)

	if err != nil {
		fmt.Print(err)
		logger.Error(err)
		return
	}
	return
}

func AdminListProduct(limit, offset, doneAt, finishedAt, productId, state int, name string) (waPro []WaProduct, count, onCount, offCount int) {
	//dbs, err := gorm.Open("mysql", "root:123456@tcp(127.0.0.1:3306)/wabao_development")
	//if err != nil {
	//	log.Fatalln(err)
	//}
	query := "SELECT id, name,total_count,coin,state,main_img,updated_at,price,imgs,detail_img,current_no FROM wabao_product WHERE deleted_at is  Null"
	queryCount := `SELECT COUNT("id") FROM wabao_product WHERE state=1 AND deleted_at is  Null`

	if productId != 0 {
		query = query + " AND id=" + strconv.Itoa(productId)
	}
	if state != 0 {
		query = query + " AND state=" + strconv.Itoa(state)
	}
	if name != "" {
		query = query + " AND name like '%" + name + "%'"
	}
	if finishedAt != 0 {
		query = query + " AND current_no between " + strconv.Itoa(doneAt) + " and " + strconv.Itoa(finishedAt)
	}
	query += " ORDER BY updated_at DESC LIMIT " + strconv.Itoa(limit) + " OFFSET " + strconv.Itoa(offset)

	num := db.Raw(queryCount).Count(&count)
	rows, err := db.Raw(query).Rows()
	if err != nil {
		fmt.Print(err)
		logger.Error(err)
		return
	}
	for rows.Next() {
		var w WaProduct
		rows.Scan(&w.ProductId, &w.Name, &w.TotalCount, &w.Coin, &w.State, &w.MainImg, &w.UpdatedAt, &w.Price, &w.Imgs, &w.DetailImg, &w.CurrentNo)
		waPro = append(waPro, w)
	}

	query2 := `SELECT COUNT("id")  FROM wabao_product WHERE state=1 AND  deleted_at is  Null`
	on := db.Raw(query2).Count(&onCount)

	query3 := `SELECT COUNT("id") FROM wabao_product WHERE state=2 AND  deleted_at is  not Null`
	off := db.Raw(query3).Count(&offCount)
	fmt.Println(num,on, off)
	return waPro, count, onCount, offCount
}

func AdminDeleteProduct(productId int) (ra int64, err error) {
	//dbs, err := gorm.Open("mysql", "root:123456@tcp(127.0.0.1:3306)/wabao_development")
	//if err != nil {
	//	log.Fatalln(err)
	//}
	DeletedAt := time.Now().Format("2006-01-02 15:04:05")
	_ = db.Exec("UPDATE wabao_product SET deleted_at=? WHERE id=?", DeletedAt, productId)
	return
}

func AdminShelfProduct(state, productId int) (ra int64, err error) {
	//dbs, err := gorm.Open("mysql", "root:123456@tcp(127.0.0.1:3306)/wabao_development")
	//if err != nil {
	//	log.Fatalln(err)
	//}
	UpdateAt := time.Now().Format("2006-01-02 15:04:05")
	_ = db.Exec("UPDATE wabao_product SET state=?,updated_at=? WHERE id=?", state, UpdateAt, productId)
	NewIssues(uint32(productId))
	return
}

func AdminUpdateProduct(Name, DetailImg, mainImg, UpdatedAt string, Price, totalCount, Coin, ProductId int, Imgs string) (ra int64, err error) {
	//dbs, err := gorm.Open("mysql", "root:123456@tcp(127.0.0.1:3306)/wabao_development")
	//if err != nil {
	//	fmt.Print(err)
	//	logger.Error(err)
	//}
	_ = db.Exec(`UPDATE wabao_product SET name=?,total_count=?,coin=?,
	main_img=?,updated_at=?,price=?,imgs=?,detail_img=? WHERE id=?`, Name, totalCount, Coin, mainImg, UpdatedAt, Price, Imgs, DetailImg, ProductId)
	if err != nil {
		fmt.Print(err)
		logger.Error(err)
		return
	}
	return
}

func AdminListIssue(limit, offset, productId int) (waIssue []WaIssue, waProduct []WaProduct, count int) {
	//dbs, err := gorm.Open("mysql", "root:123456@tcp(127.0.0.1:3306)/wabao_development")
	//if err != nil {
	//	fmt.Print(err)
	//	logger.Error(err)
	//}
	queryProduct := "SELECT  name,total_count,coin,price,main_img,id,imgs,state,detail_img,current_no FROM wabao_product WHERE id="
	queryProduct = queryProduct + strconv.Itoa(productId)

	product, err := db.Raw(queryProduct).Rows()
	if err != nil {
		fmt.Print(err)
		logger.Error(err)
		return
	}
	for product.Next() {
		var wa WaProduct
		product.Scan(&wa.Name, &wa.TotalCount, &wa.Coin, &wa.Price, &wa.MainImg, &wa.ProductId, &wa.Imgs, &wa.State, &wa.DetailImg, &wa.CurrentNo)
		waProduct = append(waProduct, wa)
	}

	queryIssue := "SELECT id,lucky_uid,product_id, total_count,coin,created_at,sold_count,state,lucky_number,finished_at,issue_no FROM wabao_issue WHERE product_id="
	queryIssue = queryIssue + strconv.Itoa(productId) + " ORDER BY finished_at DESC LIMIT " + strconv.Itoa(limit) + " OFFSET " + strconv.Itoa(offset)
	issue, err := db.Raw(queryIssue).Rows()
	if err != nil {
		fmt.Print(err)
		logger.Error(err)
		return
	}

	session := GetMongo().Clone()
	defer session.Close()
	c := session.DB(config.AppConfig.MgoDbName).C("user")
	//session := getSession()
	//c := session.DB("Post").C("user")

	for issue.Next() {
		var w WaIssue
		issue.Scan(&w.ProductId, &w.Uid, &w.Id, &w.TotalCount, &w.Coin, &w.CreatedAt, &w.SoldCount, &w.State, &w.LuckyNumber, &w.FinishedAt, &w.IssueNo)
		err := c.Find(bson.M{"uid": &w.Uid}).One(&w)
		fmt.Print("uid")
		fmt.Print(w.Uid)
		if err != nil {
			fmt.Print(err)
			logger.Error(err)
			return
		}
		issue.Scan(&w.ProductId, &w.Uid, &w.Id, &w.TotalCount, &w.Coin, &w.CreatedAt, &w.SoldCount, &w.State, &w.LuckyNumber, &w.FinishedAt, &w.IssueNo)
		w.AddPeople = w.TotalCount - w.SoldCount
		waIssue = append(waIssue, w)
	}

	queryCount := `SELECT COUNT(id) FROM wabao_issue WHERE product_id=` + strconv.Itoa(productId)
	rs := db.Raw(queryCount).Count(&count)
	fmt.Print(rs)

	return waIssue, waProduct, count
}
