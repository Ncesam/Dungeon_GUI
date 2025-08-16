import axios, { AxiosInstance } from "axios";

const API_URL = "https://example.com/api"; // твой baseURL

const $api: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true,
});

export default $api;
