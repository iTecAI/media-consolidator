import { Alert, Card, InputAdornment, TextField, Typography } from "@mui/material";
import { AccountCircle, LoginSharp, Password } from "@mui/icons-material";
import { useState } from "react";
import { post } from "../../util/api";
import { LoginResponseModel } from "../../util/models";
import { LoadingButton } from "@mui/lab";
import { useNavigate } from "react-router-dom";

export default function Login(props: {}) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [status, setStatus] = useState("running" as "running" | "error" | "success");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false as boolean);

    let nav = useNavigate();

    return (
        <Card
            sx={{
                position: "absolute",
                top: "50%",
                left: "50%",
                transform: "translate(-50%, -50%)",
                padding: "15px",
            }}
        >
            <Typography
                variant="h5"
                sx={{
                    display: "inline-block",
                    width: "100%",
                    textAlign: "center",
                    marginBottom: "10px",
                }}
            >
                Log In
            </Typography>
            <TextField
                required
                placeholder="Username"
                InputProps={{
                    startAdornment: (
                        <InputAdornment position="start">
                            <AccountCircle />
                        </InputAdornment>
                    ),
                }}
                fullWidth
                sx={{
                    marginBottom: "15px",
                }}
                value={username}
                onChange={(event) => setUsername(event.target.value)}
            />
            <TextField
                required
                type="password"
                placeholder="Password"
                InputProps={{
                    startAdornment: (
                        <InputAdornment position="start">
                            <Password />
                        </InputAdornment>
                    ),
                }}
                fullWidth
                sx={{
                    marginBottom: "15px",
                }}
                value={password}
                onChange={(event) => setPassword(event.target.value)}
            />
            {status !== "running" ? (
                <Alert
                    severity={status}
                    sx={{
                        marginBottom: "15px",
                    }}
                >
                    {error}
                </Alert>
            ) : (
                <></>
            )}
            <LoadingButton
                variant="contained"
                color="primary"
                fullWidth
                loading={loading}
                loadingPosition="start"
                startIcon={<LoginSharp />}
                onClick={() => {
                    if (username && password) {
                        setLoading(true);
                        post<LoginResponseModel>({
                            path: "/login",
                            body: { username: username, password: password },
                        }).then((result) => {
                            setLoading(false);
                            if (result.success) {
                                setStatus("success");
                                setError(
                                    `Successfully logged in as ${result.value.userInfo.username}. Redirecting...`
                                );
                                window.localStorage.setItem("sessionId", result.value.uuid);
                                nav("/", { replace: true });
                            } else {
                                setStatus("error");
                                setError(`Failed to login: ${result.reason}`);
                            }
                        });
                    } else {
                        setStatus("error");
                        setError("Please specify a username and password");
                    }
                }}
            >
                Login
            </LoadingButton>
        </Card>
    );
}
