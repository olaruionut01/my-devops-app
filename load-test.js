import http from "k6/http";
import { sleep, check } from "k6";

export const options = {
  stages: [
    { duration: "30s", target: 20 },   // ramp up to 20 users
    { duration: "60s", target: 20 },   // hold at 20 users
    { duration: "20s", target: 0  },   // ramp down
  ],
};

const BASE_URL = __ENV.BASE_URL || "http://localhost:5000";

export default function () {
  const responses = [
    http.get(`${BASE_URL}/health`),
    http.get(`${BASE_URL}/hello`),
  ];

  responses.forEach(r =>
    check(r, { "status is 200": res => res.status === 200 })
  );

  sleep(0.5);
}