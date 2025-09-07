import axios, {AxiosInstance} from "axios";

const API_URL: string = "http://92.51.38.164:8000";

const $api: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true,
});

export default $api;
