import { AppBar, Button, Toolbar, Typography } from "@mui/material";
import React, { useEffect } from "react";
import { Download } from "@mui/icons-material";
import { Box } from "@mui/system";
import "./layout.scss";
import { get, post } from "../../util/api";
import { LoginResponseModel } from "../../util/models";
import { useNavigate } from "react-router-dom";

export type LayoutProps = {
    children?: React.ReactNode;
    showLogout?: boolean;
};

export function Layout(props: LayoutProps) {
    let nav = useNavigate();

    useEffect(() => {
        get<LoginResponseModel>({ path: "/account" }).then((result) => {
            console.log(result);
            if (!result.success) {
                nav("/login", { replace: true });
            }
        });
    }, [nav]);

    return (
        <div style={{ height: "100%", width: "100%" }}>
            <Box sx={{ flexGrow: 1 }}>
                <AppBar position="static" className="noselect">
                    <Toolbar variant="dense">
                        <Download fontSize="large" sx={{ marginRight: "20px" }} />
                        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                            Consolidator
                        </Typography>
                        {props.showLogout && (
                            <Button
                                color="inherit"
                                onClick={() => {
                                    post<null>({ path: "/account/logout" }).then(() =>
                                        nav("/login", { replace: true })
                                    );
                                }}
                            >
                                Logout
                            </Button>
                        )}
                    </Toolbar>
                </AppBar>
            </Box>
            <div
                className="page-content"
                style={{ display: "inline-block", width: "100%", height: "calc(100% - 48px)" }}
            >
                {props.children ?? []}
            </div>
        </div>
    );
}
