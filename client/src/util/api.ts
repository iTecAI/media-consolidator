import { ResponseModel } from "./models";

let ROOT_URL = `${window.location.origin}/api`;

export type GetOptions = { path: string; query?: { [key: string]: any } };
export async function get<T>(options: GetOptions): Promise<ResponseModel<T>> {
    let token = window.localStorage.getItem("sessionId") || false;
    let response = await fetch(
        ROOT_URL +
            options.path +
            (options.query ? "?" + new URLSearchParams(options.query).toString() : ""),
        {
            method: "GET",
            headers: {
                Authorization: token ? `Bearer ${token}` : "Unauthorized",
            },
        }
    );

    if (response.status >= 400) {
        return {
            success: false,
            code: response.status,
            reason: (await response.json()).detail,
        };
    } else {
        return {
            success: true,
            value: await response.json(),
        };
    }
}

export type PostOptions = { path: string; query?: { [key: string]: any }; body?: any };
export async function post<T>(options: PostOptions): Promise<ResponseModel<T>> {
    let token = window.localStorage.getItem("sessionId") || false;
    let response = await fetch(
        ROOT_URL +
            options.path +
            (options.query ? "?" + new URLSearchParams(options.query).toString() : ""),
        {
            method: "POST",
            headers: {
                Authorization: token ? `Bearer ${token}` : "Unauthorized",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(options.body),
        }
    );

    if (response.status >= 400) {
        return {
            success: false,
            code: response.status,
            reason: (await response.json()).detail,
        };
    } else {
        return {
            success: true,
            value: await response.json(),
        };
    }
}
