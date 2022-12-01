(() => {
    window.AXSSignature = {
        create: async (apiBase, apiKey, details) => {
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
            return resp.data.sid;
        },
        show: (apiBase, apiKey, signeeEmail, sessionId) => {
            if (!window.__AXSSisgnaturePromise) {
                window.__AXSSisgnaturePromise = new Promise((resolve, reject) => {
                    checkSignature(apiBase, apiKey, sessionId).then(json => {
                        if (json.data.status === "SIGNED") {
                            resolve({
                                url: `${apiBase}/signature/${sessionId}/`,
                                imageUrl: `${apiBase}/signature/${sessionId}.svg`
                            });
                            delete window.__AXSSisgnaturePromise;
                        } else {
                            showModal(apiBase, signeeEmail, sessionId);
                            let interval = setInterval(() => {
                                checkSignature(apiBase, apiKey, sessionId).then(json => {
                                    if (json.data.status === "SIGNED") {
                                        clearInterval(interval);
                                        closeModal();
                                        resolve({
                                            url: `${apiBase}/signature/${sessionId}/`,
                                            imageUrl: `${apiBase}/signature/${sessionId}.svg`
                                        });
                                        delete window.__AXSSisgnaturePromise;
                                    }
                                });
                            }, 5000);
                        }
                    });
                });
            }
            return window.__AXSSisgnaturePromise;
        }
    }

    const checkSignature = (apiBase, apiKey, sessionId) => {
        let url = new URL(`/signature/${sessionId}.json`, apiBase);
        let req = fetch(url, {
            method: "GET",
            headers: { "X-Api-Key": apiKey }
        });
        return req.then(resp => resp.json());
    }

    const showModal = (apiBase, signeeEmail, sessionId) => {
        let link = document.createElement('link')
        link.rel = 'stylesheet'
        link.href = `${apiBase}/static/signature.css`;
        document.head.append(link);

        let modal = document.createElement("div");
        modal.classList.add("axs-modal-underlay")
        modal.innerHTML = `<div class="axs-modal">
            <div class="axs-modal-heading">
                <svg viewBox="0 0 111.91406 39.300781" version="1.2" width="100px" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg">
                    <title>The AXS logo</title>
                    <desc>The letters A X, and S in captial letters. The A and part of the X are a different colour to the S.</desc>>
                    <defs id="defs2360">
                        <clipPath id="clip2"><path d="M 58.867188,46.148438 54.019531,34.316406 49.171875,46.148438 Z M 50.421875,24.671875 h 7.402344 L 73.460938,61.417969 H 65.070312 L 61.734375,53.238281 H 46.304688 l -3.335938,8.179688 h -8.183594 z m 0,0" id="path1771"></path></clipPath>
                        <clipPath id="clip4"><path d="m 125.06641,23.65625 c -1.73438,0.433594 -3.28125,1.128906 -4.63672,2.082031 -1.35547,0.953125 -2.44141,2.167969 -3.25781,3.644531 -0.81641,1.472657 -1.22657,3.25 -1.22657,5.332032 0,1.875 0.38282,3.402344 1.14844,4.578125 0.76563,1.179687 1.74609,2.144531 2.94531,2.890625 1.19922,0.746094 2.54688,1.34375 4.03907,1.792968 1.49218,0.453126 2.98828,0.886719 4.48437,1.300782 1.5625,0.417968 2.91797,0.792968 4.0625,1.121094 1.14844,0.328124 2.11328,0.691406 2.89453,1.09375 0.78125,0.398437 1.36328,0.855468 1.74609,1.378906 0.38282,0.519531 0.57422,1.195312 0.57422,2.027344 0,0.902343 -0.20312,1.675781 -0.60156,2.316406 -0.39844,0.640625 -0.90234,1.152344 -1.51172,1.535156 -0.60937,0.382812 -1.28515,0.660156 -2.03125,0.832031 -0.75,0.175781 -1.48437,0.261719 -2.21484,0.261719 -2.39844,0 -4.33594,-0.539062 -5.8125,-1.617188 -1.47656,-1.074218 -2.21484,-2.882812 -2.21484,-5.421874 h -8.85938 c 0,1.878906 0.27734,3.511718 0.83203,4.902343 0.55469,1.386719 1.28516,2.59375 2.19141,3.605469 0.90234,1.019531 1.92578,1.839844 3.07422,2.472656 1.14453,0.628906 2.32031,1.136719 3.51562,1.523438 1.19922,0.382812 2.375,0.648437 3.51953,0.789062 1.14844,0.140625 2.15625,0.207032 3.02344,0.207032 1.94531,0 3.86328,-0.214844 5.75781,-0.648438 1.89453,-0.433594 3.59766,-1.128906 5.10938,-2.082031 1.51172,-0.953125 2.73828,-2.210938 3.67578,-3.773438 0.9375,-1.5625 1.40625,-3.46875 1.40625,-5.722656 0,-1.769531 -0.3125,-3.253906 -0.9375,-4.449219 -0.625,-1.199218 -1.45313,-2.195312 -2.47656,-2.992187 -1.02735,-0.800781 -2.19532,-1.449219 -3.51954,-1.953125 -1.32031,-0.503906 -2.6914,-0.945313 -4.11718,-1.328125 -1.39063,-0.34375 -2.75391,-0.675781 -4.08985,-0.988281 -1.33984,-0.3125 -2.53906,-0.667969 -3.59765,-1.066407 -1.0586,-0.398437 -1.92188,-0.882812 -2.57813,-1.457031 -0.66015,-0.574219 -1.01172,-1.328125 -1.04297,-2.261719 0,-0.800781 0.1875,-1.46875 0.57032,-2.003906 0.38281,-0.539063 0.87109,-0.964844 1.46093,-1.277344 0.58985,-0.3125 1.24219,-0.527343 1.95313,-0.648437 0.71484,-0.121094 1.38281,-0.183594 2.00781,-0.183594 0.83594,0 1.66016,0.105469 2.47656,0.3125 0.81641,0.210938 1.53907,0.539062 2.16407,0.992188 0.625,0.449218 1.12109,1.03125 1.48437,1.746093 0.36328,0.710938 0.51172,1.570313 0.44531,2.578125 h 8.44141 c -0.10547,-2.222656 -0.57422,-4.101562 -1.40625,-5.636718 -0.83594,-1.535157 -1.92969,-2.785157 -3.28516,-3.75 -1.35547,-0.960938 -2.91015,-1.65625 -4.66406,-2.074219 -1.75391,-0.421875 -3.62109,-0.632813 -5.60156,-0.632813 -1.8086,0 -3.58203,0.21875 -5.32031,0.652344" id="path1886"></path></clipPath>
                        <clipPath id="clip9"><path d="M 74.632812,30.726562 86.902344,42.996094 74.632812,55.269531 81.328125,61.964844 100.29297,42.996094 81.328125,24.03125 Z m 0,0" id="path2242"></path></clipPath>
                        <clipPath id="clip9-9"><path d="M 74.632812,30.726562 86.902344,42.996094 74.632812,55.269531 81.328125,61.964844 100.29297,42.996094 81.328125,24.03125 Z m 0,0" id="path2242-0"></path></clipPath>
                    </defs>
                    <g id="surface21905" transform="translate(-34.785156,-23.003906)">
                        <g clip-path="url(#clip8-0)" clip-rule="nonzero" id="g2380-9" class="axs-logo-fill-right" style="fill-opacity:1" transform="matrix(-1,0,0,1,187.21875,0)">
                            <g clip-path="url(#clip9-9)" clip-rule="nonzero" id="g2378-9" class="axs-logo-fill-right" style="fill-opacity:1">
                                <path class="axs-logo-fill-right" style="fill-opacity:1;fill-rule:nonzero;stroke:none" d="M 74.632812,24.03125 V 61.964844 H 100.29297 V 24.03125 Z m 0,0" id="path2376-9"></path>
                            </g>
                        </g>
                        <g clip-path="url(#clip1)" clip-rule="nonzero" id="g2366" class="axs-logo-fill-left" style="fill-opacity:1">
                            <g clip-path="url(#clip2)" clip-rule="nonzero" id="g2364" class="axs-logo-fill-left" style="fill-opacity:1">
                                <path class="axs-logo-fill-left" style="fill-opacity:1;fill-rule:nonzero;stroke:none" d="M 34.785156,24.671875 V 61.417969 H 73.460938 V 24.671875 Z m 0,0" id="path2362"></path>
                            </g>
                        </g>
                        <g clip-path="url(#clip3)" clip-rule="nonzero" id="g2372" class="axs-logo-fill-right" style="fill-opacity:1">
                            <g clip-path="url(#clip4)" clip-rule="nonzero" id="g2370" class="axs-logo-fill-right" style="fill-opacity:1">
                                <path class="axs-logo-fill-right" style="fill-opacity:1;fill-rule:nonzero;stroke:none" d="M 146.69922,62.304688 V 23.003906 h -32.10547 v 39.300782 z m 0,0" id="path2368"></path>
                            </g>
                        </g>
                        <g clip-path="url(#clip8)" clip-rule="nonzero" id="g2380" class="axs-logo-fill-left" style="fill-opacity:1">
                            <g clip-path="url(#clip9)" clip-rule="nonzero" id="g2378" class="axs-logo-fill-left" style="fill-opacity:1">
                                <path class="axs-logo-fill-left" style="fill-opacity:1;fill-rule:nonzero;stroke:none" d="M 74.632812,24.03125 V 61.964844 H 100.29297 V 24.03125 Z m 0,0" id="path2376"></path>
                            </g>
                        </g>
                    </g>
                </svg>
                <h2><span class="sr-only">AXS</span> Signature</h2>
                <button aria-label="Close" type="button" class="axs-modal-close-button">
                    <svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16">
                        <path fill-rule="evenodd" d="M3.72 3.72a.75.75 0 011.06 0L8 6.94l3.22-3.22a.75.75 0 111.06 1.06L9.06 8l3.22 3.22a.75.75 0 11-1.06 1.06L8 9.06l-3.22 3.22a.75.75 0 01-1.06-1.06L6.94 8 3.72 4.78a.75.75 0 010-1.06z"></path>
                    </svg>
                </button>
            </div>
            <div class="axs-modal-body">
                <p>We've sent an email to <strong>${signeeEmail}</strong>, check your inbox for a secure link.</p>
                <div class="axs-modal-loading"><div></div><div></div><div></div><div></div></div>
                <p>Your unique session ID is</p>
                <p class="session-id"><strong>${sessionId}</strong></p>
                <p>You can use this to check that you're signing the right document.</p>
                <p class="smallprint"><small><a target="_blank" href='${apiBase}'>What is AXS Signature?</a> &middot; <a target="_blank" href='${apiBase}/terms/'>Terms and Conditions</a> &middot; <a target="_blank" href='${apiBase}/privacy/'>Privacy Notice</a>
            </div>
        </div>`;

        document.addEventListener("click", onClick);
        document.addEventListener("keyup", onKeyUp);
        document.body.append(modal);
        document.body.classList.add("axs-modal-open");
    }

    const onClick = (evt) => {
        if (evt.target.closest(".axs-modal-close-button") || !evt.target.closest(".axs-modal")) {
            closeModal();
        }
    }

    const onKeyUp = (evt) => {
        evt = evt || window.event;
        var isEscape = false;
        if ("key" in evt) {
            isEscape = (evt.key === "Escape" || evt.key === "Esc");
        } else {
            isEscape = (evt.keyCode === 27);
        }
        if (isEscape) {
            closeModal();
        }
    }

    const closeModal = () => {
        document.body.classList.remove("axs-modal-open");
        const modal = document.querySelector(".axs-modal-underlay")
        modal.parentNode.removeChild(modal);
        document.removeEventListener("click", onClick);
        document.removeEventListener("keyup", onKeyUp);
    }
})();