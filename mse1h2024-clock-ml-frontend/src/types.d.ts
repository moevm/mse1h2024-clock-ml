export type TToolbar = {
	tool: "brush" | "eraser";
	size: number;
};

export type TTools = "brush" | "eraser";

export interface IEstimationResponse {
	result: number;
}
