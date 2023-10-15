import axios from "axios";


const BASE_URL = process.env.REACT_APP_API_URL;

export const sendAuthRequest = (url, data) => {
	return axios({
		method: 'POST',
		url: BASE_URL + url,
		data: data,
		headers: {
			'Content-Type': 'application/json',
		}
	});
};

export const sendGetRequest = (url, accessToken) => {
	return axios({
		method: 'GET',
		url: BASE_URL + url,
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${accessToken}`
		}
	});
};

export const sendPostRequest = (url, data, accessToken, hasFile = false) => {
	return axios({
		method: 'POST',
		url: BASE_URL + url,
		data: data,
		headers: {
			'Content-Type': hasFile ? 'multipart/form-data' : 'application/json',
			Authorization: `Bearer ${accessToken}`
		}
	});
};

export const sendPatchRequest = (url, data, accessToken, hasFile = false) => {
	return axios({
		method: 'PATCH',
		url: BASE_URL + url,
		data: data,
		headers: {
			'Content-Type': hasFile ? 'multipart/form-data' : 'application/json',
			Authorization: `Bearer ${accessToken}`
		}
	});
};

export const sendDeleteRequest = (url, accessToken) => {
	return axios({
		method: 'DELETE',
		url: BASE_URL + url,
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${accessToken}`
		}
	});
};
