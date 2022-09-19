(() => {
    window.requestSignature = async (apiBase, apiKey, details) => {
        let url = new URL("/session/", apiBase);
        let resp = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json;charset=utf-8",
                "X-Api-Key": apiKey
            },
            body: JSON.stringify(details)
        });
        resp = await resp.json();

        window.alert("You just got an email!");
    }
})();
