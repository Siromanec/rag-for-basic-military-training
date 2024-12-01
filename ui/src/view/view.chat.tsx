import React, {useState} from "react";
import {Box, TextField, Button, Typography, Paper} from "@mui/material";
import {Message, MessageService} from "../service/service.message";
import DeleteForeverIcon from '@mui/icons-material/DeleteForever';
// Define the types for a message


const Chat: React.FC = () => {
    const [messageService] = useState<MessageService>(new MessageService());

    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState<string>("");

    // Handle sending a message
    const handleSend = () => {
        if (input.trim() === "") return;

        messageService.addMessage(input).then(() => {
            setTimeout(() => {
            setMessages(messageService.messages);
            }, 1000);
        })
        setInput("");
    };

    return (
        <Paper
            elevation={3}
            sx={{
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
                width: "70%",
                height: "90vh",
                margin: "auto",
                borderRadius: 2,
                overflow: "hidden",
            }}
        >
            {/* Messages Section */}
            <Box
                sx={{
                    flex: 1,
                    overflowY: "auto",
                    padding: 2,
                    backgroundColor: "#bfa991",
                }}
                whiteSpace={"pre-wrap"}
            >
                {messageService.messages.map((message: Message, index: number) => (
                    <Box
                        key={index}
                        sx={{
                            display: "flex",
                            justifyContent:
                                message.sender === "user" ? "flex-end" : "flex-start",
                            marginBottom: 1,
                        }}
                    >
                        <Box
                            sx={{
                                maxWidth: "75%",
                                padding: 1.5,
                                borderRadius: 2,
                                backgroundColor:
                                    message.sender === "user" ? "#8a7e68" : "#584f3e",
                                textAlign: message.sender === "bot" && message.imageUrl ? "center" : "left",
                            }}
                        >
                            {message.text && (
                                <Typography  variant="body1" color={message.sender === "user" ? "black" : "wheat"}>{message.text}</Typography>
                            )}
                            {message.imageUrl && (
                                <Box
                                    component="img"
                                    src={message.imageUrl}
                                    alt="Bot response"
                                    sx={{ maxWidth: "100%", borderRadius: 2, marginTop: 1 }}
                                />
                            )}
                        </Box>
                    </Box>
                ))}
            </Box>

            {/* Input Section */}
            <Box
                sx={{
                    display: "flex",
                    padding: 2,
                    borderTop: "1px solid #584f3e",
                    backgroundColor: "#8a7e68",
                }}
            >
                <Button
                    variant="contained"
                    color="primary"
                    onClick={() => {messageService.clearMessages(); setMessages([])}}
                    disabled={messages.length === 0}
                >
                    <DeleteForeverIcon/></Button>
                <TextField
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type your message..."
                    onKeyDown={(e) => {
                        if (e.key === "Enter") {
                            e.preventDefault(); // Prevent default form submission behavior
                            handleSend(); // Trigger send functionality
                        }
                    }}
                    variant="outlined"
                    fullWidth
                    size="small"
                    sx={{marginRight: 1}}
                />
                <Button
                    variant="contained"
                    color="primary"
                    onClick={handleSend}
                    disabled={!input.trim()}
                >
                    Send
                </Button>
            </Box>
        </Paper>
    );
};

export default Chat;
