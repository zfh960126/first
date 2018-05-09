package controller

import (
	"wa_server/lib/status"
	"wa_server/model"

	"github.com/codinl/go-logger"
	"github.com/gin-gonic/gin"

	"fmt"
	"log"
	"time"
	"encoding/json"
)

/**
* @api {post} admin/wabao/product/add
* @apiName add
* @apiGroup admin
* @apiPermission 需要登录
* @apiParam {int} ProductId 商品ID
* @apiParam {string} Name  商品名字
* @apiParam {int} TotalCount  所需多少个号码
* @apiParam {int} Coin 每个号码多少金币
* @apiParam {string} MainImg 商品缩略图
* @apiParam {string} CreatedAt  创建时间
* @apiParam {string} UpdatedAt  更新时间
* @apiParam {int} Price	价值
* @apiParam {string} Imgs		轮播图
* @apiParam {string} DetailImg		细节图
*
* @apiSuccessExample {json} 成功返回
* {
*	code: 200,
	desc: "成功",
	data: 0
* }
* @apiUse Error_default
*/
func AdminWabaoProductAdd(c *gin.Context) {
	req := struct {
		Name       string   `json:"name" form:"name"`
		TotalCount uint32   `json:"total_count" form:"total_count"`
		Coin       uint32   `json:"coin" form:"coin"`
		MainImg    string   `json:"main_img" form:"main_img"`
		Price      uint32   `json:"price" form:"price"`
		Imgs       []string `json:"imgs" form:"imgs"`
		DetailImg  string   `json:"detail_img" form:"detail_img"`
	}{}
	if err := c.BindJSON(&req); err != nil {
		logger.Error(err)
		RespJson(c, status.BadRequest, nil)
		return
	}

	body, err := json.Marshal(req.Imgs)
	if err != nil {
		logger.Error(err)
		RespJson(c, status.BadRequest, nil)
		return
	}

	imgs := string(body)
	product := model.WabaoProduct{
		Name:       req.Name,
		TotalCount: req.TotalCount,
		Coin:       req.Coin,
		MainImg:    req.MainImg,
		Price:      req.Price,
		Imgs:       imgs,
		DetailImg:  req.DetailImg,
		State:      model.STATE_DOWN_SHELVES,
	}
	db := model.DbGet()
	err = product.Create(db)
	if err != nil {
		logger.Error(err)
		RespJson(c, status.DBOperateError, nil)
		return
	}

	RespJson(c, status.OK, product)
}

/**
* @api {post} admin/wabao/product/list
* @apiName list
* @apiGroup admin
* @apiPermission 需要登录
* @apiParam {int} ProductId 商品ID
* @apiParam {string} Name  商品名字
* @apiParam {int} State  商品状态（上线,下线）
* @apiParam {int} LeftTimes  搜索开奖次数
* @apiParam {int} RightTimes 搜索开奖次数
*
* @apiSuccessExample {json} 成功返回
*
*{
	"code": 200,
	"desc": "成功",
	"data": {
		"wa": [{
			"product_id": 12,
			"name": "sdfgdh",
			"total_count": 1234,
			"coin": 342,
			"state": 2,
			"main_img": "https://static.wawa.gongfutingche.com/coverkey_1524222969145",
			"updated_at": "2018-04-20 19:26:38",
			"price": 1,
			"imgs": "[\"https://static.wawa.gongfutingche.com/bannerkey_1524222971268\"]",
			"detail_img": "https://static.wawa.gongfutingche.com/detailskey_1524222975184",
			"current_no": 0
		}, ...
		"count": 4,
		"onCount": 1,
		"offCount": 3

	}
}

*
* @apiUse Error_default
*/
func AdminWabaoProductList(c *gin.Context) {
	req := struct {
		ProductId  int    `json:"product_id"`
		Name       string `json:"name"`
		State      int    `json:"state"`
		LeftTimes  int    `json:"left_times"`
		RightTimes int    `json:"right_times"`
		Limit      int    `json:"limit" form:"limit"`
		Offset     int    `json:"offset" form:"offset"`
	}{}
	if err := c.BindJSON(&req); err != nil {
		fmt.Print(err)
		logger.Error(err)
		return
	}

	wa, count, onCount, offCount := model.AdminListProduct(req.Limit, req.Offset, req.LeftTimes, req.RightTimes, req.ProductId, req.State, req.Name)
	type WaProduct struct {
		ProductId  int    `json:"product_id" form:"product_id"`
		Name       string `json:"name" form:"name"`
		TotalCount int    `json:"total_count" form:"total_count"`
		Coin       int    `json:"coin" form:"coin"`
		State      int    `json:"state" form:"state"`
		MainImg    string `json:"main_img" form:"main_img"`
		UpdatedAt  string `json:"updated_at" form:"updated_at"`
		Price      int    `json:"price" form:"price"`
		Imgs       string `json:"imgs" form:"imgs"`
		DetailImg  string `json:"detail_img" form:"detail_img"`
		CurrentNo  int    `json:"current_no" form:"current_no"`
	}

	var datas []*WaProduct
	for _, v := range wa {
		waPro := &WaProduct{
			ProductId:  v.ProductId,
			Name:       v.Name,
			TotalCount: v.TotalCount,
			Coin:       v.Coin,
			State:      v.State,
			MainImg:    v.MainImg,
			UpdatedAt:  v.UpdatedAt,
			Price:      v.Price,
			Imgs:       v.Imgs,
			DetailImg:  v.DetailImg,
			CurrentNo:  v.CurrentNo,
		}
		datas = append(datas, waPro)
	}

	result := struct {
		Wa       []*WaProduct `json:"wa"`
		Count    int          `json:"count"`
		OnCount  int          `json:"onCount"`
		OffCount int          `json:"offCount"`
	}{
		Wa:       datas,
		Count:    count,
		OnCount:  onCount,
		OffCount: offCount,
	}
	RespJson(c, status.OK, result)
}

/**
* @api {post} admin/wabao/product/delete
* @apiName delete
* @apiGroup admin
* @apiPermission 需要登录
* @apiParam {int} ProductId 商品ID
*
* @apiSuccessExample {json} 成功返回
* {
*	code: 200,
	desc: "成功",
	data: "Delete successful [1 2]"
* }
* @apiUse Error_default
*/
func AdminWabaoProductDelete(c *gin.Context) {
	req := struct {
		ProductId []int `json:"product_id"`
	}{}
	if err := c.BindJSON(&req); err != nil {
		logger.Error(err)
		RespJson(c, status.BadRequest, nil)
		return
	}

	for _, id := range req.ProductId {
		model.AdminDeleteProduct(id)
	}
	msg := fmt.Sprintf("Delete successful %d", req.ProductId)
	RespJson(c, status.OK, msg)
}

/**
* @api {post} admin/wabao/product/shelf
* @apiName shelf
* @apiGroup admin
* @apiPermission 需要登录
* @apiParam {int} ProductId 商品ID
* @apiParam {int} State  商品状态（上线,下线）
*
* @apiSuccessExample {json} 成功返回
* {
*	code: 200,
	desc: "成功",
	data: "Shelf successful 12"
* }
* @apiUse Error_default
*/
func AdminWabaoProductShelf(c *gin.Context) {
	req := struct {
		ProductId int `json:"product_id"`
		State     int `json:"state"`
	}{}
	if err := c.BindJSON(&req); err != nil {
		logger.Error(err)
		RespJson(c, status.BadRequest, nil)
		return
	}
	model.AdminShelfProduct(req.State, req.ProductId)
	msg := fmt.Sprintf("Shelf successful %d", req.ProductId)
	RespJson(c, status.OK, msg)
}

//
//func AdminCountProductApi(c *gin.Context) {
//
//	req := struct {
//		State int `json:"state"`
//	}{}
//
//	if err := c.BindJSON(&req); err != nil {
//		fmt.Print(err)
//		logger.Error(err)
//		return
//	}
//
//	Count, err := model.AdminCountProduct(req.State)
//	if err != nil {
//		log.Fatalln(err)
//	}
//	c.JSON(http.StatusOK, gin.H{
//		"Count": Count,
//	})
//	return
//}

/**
* @api {post} admin/wabao/product/update
* @apiName update
* @apiGroup admin
* @apiPermission 需要登录
* @apiParam {int} ProductId 商品ID
* @apiParam {string} Name  商品名字
* @apiParam {int} TotalCount  所需多少个号码
* @apiParam {int} Coin 每个号码多少金币
* @apiParam {string} MainImg 商品缩略图
* @apiParam {string} CreatedAt  创建时间
* @apiParam {string} UpdatedAt  更新时间
* @apiParam {int} Price	价值
* @apiParam {string} Imgs		轮播图
* @apiParam {string} DetailImg		细节图
* @apiParam {int} State  商品状态（上线,下线）
*
* @apiSuccessExample {json} 成功返回
* {
*	code: 200,
	desc: "成功",
	data: "update successful 0"
* }
* @apiUse Error_default
*/
func AdminWabaoProductUpdate(c *gin.Context) {
	req := struct {
		ProductId   int    `json:"product_id"`
		Name        string `json:"name"`
		Description string `json:"description"`
		TotalCount  int    `json:"total_count" form:"total_count"`
		Coin        int    `json:"coin" form:"coin"`
		State       int    `json:"state"`
		MainImg     string `json:"main_img"`
		CreatedAt   string `json:"created_at"`
		UpdatedAt   string `json:"updated_at"`
		Price       int    `json:"price"`
		Imgs        string `json:"imgs"`
		DetailImg   string `json:"detail_img"`
	}{}
	if err := c.BindJSON(&req); err != nil {
		fmt.Print(err)
		logger.Error(err)
		return
	}

	UpdatedAt := time.Now().Format("2006-01-02 15:04:05")
	_, err := model.AdminUpdateProduct(req.Name, req.DetailImg, req.MainImg, UpdatedAt, req.Price, req.TotalCount, req.Coin, req.ProductId, req.Imgs)
	if err != nil {
		fmt.Print(err)
		log.Fatalln(err)
	}

	msg := fmt.Sprintf("update successful %d", req.ProductId)
	RespJson(c, status.OK, msg)
}

/**
* @api {post} v1/admin/wabao/issue/list
* @apiName list
* @apiGroup admin
* @apiPermission 需要登录
* @apiParam {int} ProductId 商品ID
*
* @apiSuccessExample {json} 成功返回
* {
*	"code": 200,
	"desc": "成功",
	"data": {
		"wa": [{
			"product_id": 1,
			"id": 0,
			"name": "safdsfasdf",
			"description": "",
			"total_count": 100,
			"coin": 10,
			"main_img": "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
			"created_at": "",
			"updated_at": "",
			"deleted_at": "",
			"price": 424,
			"imgs": "[\"https://static.wawa.gongfutingche.com/bannerkey_1524210414254\",\"https://static.wawa.gongfutingche.com/bannerkey_1524210429423\",\"https://static.wawa.gongfutingche.com/bannerkey_1524210420420\",\"https://static.wawa.gongfutingche.com/bannerkey_1524210425191\",\"https://static.wawa.gongfutingche.com/bannerkey_1524210445461\"]",
			"detail_img": "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
			"sold_count": 0,
			"nick_name": "agasgsz",
			"tel": "15385381996",
			"state": 1,
			"lucky_number": 424,
			"current_no": 14,
			"finished_at": "2018-04-14 21:24:21",
			"issue_no": 1212,
			"add_people": 424
		}...
	]
	}
* }
* @apiUse Error_default
*/
func AdminWabaoIssueList(c *gin.Context) {
	req := struct {
		ProductId int `json:"product_id"`
		Limit     int `json:"limit" form:"limit"`
		Offset    int `json:"offset" form:"offset"`
	}{}
	if err := c.BindJSON(&req); err != nil {
		fmt.Print(err)
		logger.Error(err)
		return
	}

	waIssue, waProduct, count := model.AdminListIssue(req.Limit, req.Offset, req.ProductId)
	type Wa struct {
		ProductId   int    `json:"product_id" form:"product_id"`
		Id          int    `json:"id" form:"id"`
		Name        string `json:"name" form:"name"`
		Description string `json:"description" form:"description"`
		TotalCount  int    `json:"total_count" form:"total_count"`
		Coin        int    `json:"coin" form:"coin"`
		MainImg     string `json:"main_img" form:"main_img"`
		CreatedAt   string `json:"created_at" form:"created_at"`
		UpdatedAt   string `json:"updated_at" form:"updated_at"`
		DeletedAt   string `json:"deleted_at" form:"deleted_at"`
		Price       int    `json:"price" form:"price"`
		Imgs        string `json:"imgs" form:"imgs"`
		DetailImg   string `json:"detail_img" form:"detail_img"`
		SoldCount   int    `json:"sold_count" form:"sold_count"`
		NickName    string `json:"nick_name" form:"nick_name"`
		Tel         string `json:"tel" form:"tel"`
		State       int    `json:"state" form:"state"`
		LuckyNumber uint32 `json:"lucky_number" form:"lucky_number"`
		CurrentNo   int    `json:"current_no" form:"current_no"`
		FinishedAt  string `json:"finished_at" form:"finished_at"`
		IssueNo     int    `json:"issue_no" form:"issue_no"`
		AddPeople   int    `json:"add_people" form:"add_people"`
	}

	var data []*Wa
	for _, P := range waProduct {
		for _, I := range waIssue {
			WaIss := &Wa{
				LuckyNumber: I.LuckyNumber,
				SoldCount:   I.SoldCount,
				NickName:    I.NickName,
				Tel:         I.Tel,
				State:       I.State,
				AddPeople:   I.AddPeople,
				FinishedAt:  I.FinishedAt,
				IssueNo:     I.IssueNo,
				ProductId:   P.ProductId,
				Name:        P.Name,
				Price:       P.Price,
				CurrentNo:   P.CurrentNo,
				TotalCount:  P.TotalCount,
				Coin:        P.Coin,
				MainImg:     P.MainImg,
				DetailImg:   P.DetailImg,
				Imgs:        P.Imgs,
			}
			data = append(data, WaIss)
		}
	}

	result := struct {
		Wa    []*Wa `json:"wa"`
		Count int   `json:"count"`
	}{
		Wa:    data,
		Count: count,
	}
	RespJson(c, status.OK, result)
}
