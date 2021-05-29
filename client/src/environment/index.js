const axios = require("axios");

export const flaskBackendService = axios.create({
  baseURL: "/"
});
