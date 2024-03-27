import { BASE_URL } from "../constants/url";
import { checkResponse } from "./check-response";

export async function sendForm<T>(url: string, formData: FormData) {
	return fetch(`${BASE_URL}${url}`, {
		method: "POST",
		body: formData,
	}).then<T>(checkResponse<T>);
}
