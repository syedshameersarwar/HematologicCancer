import {
    flaskBackendService,
} from "../evironment/environment";

class ApiService {
    get(data) {
        return flaskBackendService.request({
            method: "get",
            url: data.url, 
            params: data.params
        });
    }
    post(data) {
        return flaskBackendService.request({
            headers: data.headers,
            method: "post",
            url: data.url,
            data: data.body
        });
    }
}
export default new ApiService();