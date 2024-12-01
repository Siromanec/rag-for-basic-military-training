
import { singleton } from "tsyringe";
import { makeObservable, observable } from 'mobx';
import { v4 as uuidv4 } from 'uuid';

export interface Message {
    sender: "user" | "bot";
    text?: string;
    imageUrl?: string;
    conversationId: string;
}


@singleton()
export class MessageService {
    get endpoint(): string {
        return this._endpoint;
    }

    set endpoint(value: string) {
        this._endpoint = value;
    }
    get messages(): Message[] {
        return this._messages;
    }
    @observable private _messages: Message[] = [];
    private _endpoint: string;
    private readonly baseUrl: string;
    private readonly hostname: string;
    private readonly endpointName: string;
    private readonly port: number;

    private conversationId: string;

    constructor(
    ) {
        makeObservable(this);
        this.hostname = window.location.hostname;
        this.port = 8000;
        this.baseUrl = '';
        this.endpointName = '';
        this._endpoint = `http://${this.hostname}:${this.port}${this.baseUrl}${this.endpointName}`;
        this.conversationId = uuidv4();
    }

    addMessage = async (text: string) => {
        this._messages.push({sender: "user", text: text, conversationId: this.conversationId});
        return fetch(`${this._endpoint}/generate-response`, {
            method: "POST",
            body: JSON.stringify(this._messages),
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then(response => response.json())
            .then(data => this._messages = data)
            .catch(error => console.error(error));
    }

    clearMessages() {
        this._messages = [];
        this.conversationId = uuidv4();
    }
}