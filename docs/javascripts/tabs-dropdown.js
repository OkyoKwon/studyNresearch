(function () {
  "use strict";

  var DROPDOWNS = {
    "결제/금융 인프라": [
      { label: "PG (Payment Gateway)", path: "domains/pg-service/" },
      { label: "MOR (Merchant of Record)", path: "domains/mor-service/" },
      { label: "오픈뱅킹 / BaaS", path: "domains/open-banking/" },
      { label: "BNPL (Buy Now Pay Later)", path: "domains/bnpl/" },
      { label: "임베디드 금융", path: "domains/embedded-finance/" },
      { label: "실시간 결제 인프라", path: "domains/realtime-payment/" }
    ],
    "디지털 자산/Web3": [
      { label: "가상자산 규제", path: "domains/crypto-regulation/" },
      { label: "스테이블코인 규제", path: "domains/stablecoin-regulation/" },
      { label: "CBDC (중앙은행 디지털화폐)", path: "domains/cbdc/" },
      { label: "토큰증권 (STO)", path: "domains/sto/" },
      { label: "DeFi 프로토콜", path: "domains/defi/" }
    ],
    "규제/컴플라이언스": [
      { label: "AML/KYC", path: "domains/aml-kyc/" },
      { label: "데이터 규제 (개인정보)", path: "domains/data-regulation/" },
      { label: "레그테크 (RegTech)", path: "domains/regtech/" }
    ],
    "비즈니스 모델": [
      { label: "SaaS 비즈니스 모델", path: "domains/saas-business/" },
      { label: "플랫폼 이코노미", path: "domains/platform-economy/" }
    ]
  };

  function getBaseUrl() {
    // Use __md_scope set by MkDocs Material
    if (typeof __md_scope !== "undefined") {
      return __md_scope.href;
    }
    // Fallback: derive from the "홈" tab's href
    var homeTab = document.querySelector('.md-tabs__link[href$="/"], .md-tabs__link[href="."], .md-tabs__link[href="./"]');
    if (homeTab) {
      var a = document.createElement("a");
      a.href = homeTab.getAttribute("href");
      return a.href.replace(/\/$/, "") + "/";
    }
    return window.location.origin + "/";
  }

  function buildDropdowns() {
    // Remove old dropdowns
    document.querySelectorAll(".tabs-dropdown").forEach(function (el) {
      el.remove();
    });
    document.querySelectorAll(".tabs-dropdown-parent").forEach(function (el) {
      el.classList.remove("tabs-dropdown-parent");
    });

    var baseUrl = getBaseUrl();
    if (!baseUrl.endsWith("/")) baseUrl += "/";

    var tabs = document.querySelectorAll(".md-tabs__link");
    tabs.forEach(function (tab) {
      // Extract text, stripping whitespace and inner elements
      var text = tab.textContent.replace(/\s+/g, " ").trim();
      var items = DROPDOWNS[text];
      if (!items) return;

      var tabItem = tab.parentElement;
      tabItem.classList.add("tabs-dropdown-parent");

      var dropdown = document.createElement("ul");
      dropdown.className = "tabs-dropdown";

      items.forEach(function (item) {
        var li = document.createElement("li");
        var a = document.createElement("a");
        a.href = baseUrl + item.path;
        a.textContent = item.label;
        li.appendChild(a);
        dropdown.appendChild(li);
      });

      tabItem.appendChild(dropdown);
    });
  }

  // Run on initial load
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", buildDropdowns);
  } else {
    buildDropdowns();
  }

  // Re-run after instant navigation page changes
  if (typeof document$ !== "undefined") {
    document$.subscribe(function () {
      buildDropdowns();
    });
  } else {
    // Fallback: observe for instant navigation via MutationObserver
    var observer = new MutationObserver(function () {
      if (document.querySelector(".md-tabs__link") && !document.querySelector(".tabs-dropdown")) {
        buildDropdowns();
      }
    });
    observer.observe(document.body, { childList: true, subtree: true });
  }
})();
