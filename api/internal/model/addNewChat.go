package model

type AddNewChat struct {
	ChatId      int    `json:"chat_id"`
	OwnerId     int    `json:"owner_id"`
	Price       int    `json:"price"`
	Name        string `json:"name"`
	Description string `json:"description"`
}
