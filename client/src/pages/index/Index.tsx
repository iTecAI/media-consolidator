import { Search } from "@mui/icons-material";
import { Divider, TextField, InputAdornment, ButtonGroup, Button } from "@mui/material";
import { Box } from "@mui/material";
import { useState } from "react";
import { get, post } from "../../util/api";
import "./index.scss";

type ActiveMode = "torrents" | "podcasts" | "youtube" | "music" | "books";
//const modes: ActiveMode[] = ["torrents", "podcasts", "youtube", "music", "books"];

function ModeButton(props: {
    mode: ActiveMode;
    activeModes: ActiveMode[];
    setActiveModes: (modes: ActiveMode[]) => void;
}) {
    let { mode, activeModes, setActiveModes } = props;
    return (
        <Button
            variant={activeModes.includes(mode) ? "contained" : "outlined"}
            onClick={() => {
                let newModes: ActiveMode[] = [];
                if (activeModes.includes(mode)) {
                    for (let m of activeModes) {
                        if (m !== mode) {
                            newModes.push(m);
                        }
                    }
                } else {
                    newModes = JSON.parse(JSON.stringify(activeModes));
                    newModes.push(mode);
                }
                setActiveModes(newModes);
            }}
        >
            {mode}
        </Button>
    );
}

function search(term: string, modes: ActiveMode[]) {
    for (let mode of modes) {
        switch (mode) {
            case "podcasts":
                get({ path: "/sources/podcasts/search", query: { q: term } }).then(console.log);
        }
    }
}

export default function IndexPage() {
    const [activeModes, setActiveModes] = useState([] as ActiveMode[]);

    return (
        <Box sx={{ width: "100%", height: "100%" }}>
            <Box sx={{ height: "48px", position: "relative" }}>
                <TextField
                    InputProps={{
                        startAdornment: (
                            <InputAdornment position="start">
                                <Search />
                            </InputAdornment>
                        ),
                    }}
                    variant="outlined"
                    size="small"
                    placeholder="Search"
                    className="main-search"
                    onKeyDown={(event) => {
                        if (event.key === "Enter") {
                            search((event.target as any).value, activeModes);
                        }
                    }}
                />
                <ButtonGroup className="mode-buttons">
                    <ModeButton
                        mode={"torrents"}
                        activeModes={activeModes}
                        setActiveModes={setActiveModes}
                    />
                    <ModeButton
                        mode={"podcasts"}
                        activeModes={activeModes}
                        setActiveModes={setActiveModes}
                    />
                    <ModeButton
                        mode={"youtube"}
                        activeModes={activeModes}
                        setActiveModes={setActiveModes}
                    />
                    <ModeButton
                        mode={"music"}
                        activeModes={activeModes}
                        setActiveModes={setActiveModes}
                    />
                    <ModeButton
                        mode={"books"}
                        activeModes={activeModes}
                        setActiveModes={setActiveModes}
                    />
                </ButtonGroup>
            </Box>
            <Divider />
        </Box>
    );
}
