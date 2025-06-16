// Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
// SPDX-License-Identifier: MIT

import { env } from "~/env";

export function resolveServiceURL(path: string) {
  // let BASE_URL =  "/api/ai_chat/api/deer-flow";
  let BASE_URL =  "http://localhost:8000/api";
  if (!BASE_URL.endsWith("/")) {
    BASE_URL += "/";
  }
  if (BASE_URL.startsWith("http")) {
    return new URL(path, BASE_URL).toString();
  }
  return BASE_URL + path
}

