package restapi

type SuccessResponse struct {
	Result int `json:"result"`
}

type ErrorResponse struct {
	Error string `json:"error"`
}
