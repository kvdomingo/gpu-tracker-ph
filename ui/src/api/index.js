import axios from "axios";

const baseURL = "/api/";

const axi = axios.create({ baseURL });

const api = {
  get() {
    return axi.get("/");
  },
};

export default api;
