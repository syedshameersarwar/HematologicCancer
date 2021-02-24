import api from "../services/api-service";

class TestService {
    testPythonApi() {
        try {
            return api.get({
                url: "flask/get-response",
            });
        } catch (error) {
            return new Error(error);
        }
    }
}
export default new TestService();