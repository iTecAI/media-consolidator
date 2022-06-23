import { AppBar, Button, Toolbar, Typography } from "@mui/material";
import React from "react";
import { Download } from "@mui/icons-material";
import { Box } from "@mui/system";
import "./layout.scss";

export type LayoutProps = {
    children?: React.ReactNode;
    showLogout?: boolean;
    showTabs?: boolean;
};

export function Layout(props: LayoutProps) {
    return (
        <div>
            <Box sx={{ flexGrow: 1 }}>
                <AppBar position="static" className="noselect">
                    <Toolbar>
                        <Download fontSize="large" sx={{ marginRight: "20px" }} />
                        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                            Consolidator
                        </Typography>
                        {props.showLogout && <Button color="inherit">Logout</Button>}
                    </Toolbar>
                </AppBar>
            </Box>
            <div className="page-content">{props.children ?? []}</div>
        </div>
    );
}
