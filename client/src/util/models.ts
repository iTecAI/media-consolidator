export type ResponseModel<T> =
    | { success: false; code: number; reason: string }
    | { success: true; value: T };

export type UserInfoResourceModel = {
    username: string | null;
    email: string | null;
    displayName: string | null;
    icon: string | null;
};

export type LoginResponseModel = {
    uuid: string;
    permissions: string[];
    userInfo: UserInfoResourceModel;
};
