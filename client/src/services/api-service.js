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
            method: "post",
            url: data.url,
            params: data.params
        });
    }
}
export default new ApiService();