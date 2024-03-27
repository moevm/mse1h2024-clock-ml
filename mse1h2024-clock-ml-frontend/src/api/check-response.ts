export async function checkResponse<T>(res: Response): Promise<T> {
	if (res.ok) {
		return res.json();
	}

	return Promise.reject(await res.json());
}
