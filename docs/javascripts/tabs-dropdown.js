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

  function findBaseUrl() {
    // Method 1: Find "홈" tab and resolve its href as the site root
    var homeTab = document.querySelector('.md-tabs__link');
    if (homeTab) {
      var tabs = document.querySelectorAll('.md-tabs__link');
      for (var i = 0; i < tabs.length; i++) {
        if (tabs[i].textContent.replace(/\s+/g, " ").trim() === "홈") {
          // Create a temporary anchor to resolve the relative href to absolute
          var a = document.createElement("a");
          a.href = tabs[i].getAttribute("href");
          var resolved = a.href;
          // Ensure trailing slash
          if (!resolved.endsWith("/")) resolved += "/";
          return resolved;
        }
      }
    }
    // Method 2: Use __md_scope
    if (typeof __md_scope !== "undefined") {
      return __md_scope.href;
    }
    return window.location.origin + "/";
  }

  function buildDropdowns() {
    var baseUrl = findBaseUrl();

    var tabs = document.querySelectorAll(".md-tabs__link");
    if (!tabs.length) return;

    tabs.forEach(function (tab) {
      var tabItem = tab.parentElement;
      if (tabItem.querySelector(".tabs-dropdown")) return;

      var text = tab.textContent.replace(/\s+/g, " ").trim();
      var items = DROPDOWNS[text];
      if (!items) return;

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

  // Run when DOM is ready
  function init() {
    buildDropdowns();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  // Also run on window load as safety net
  window.addEventListener("load", init);

  // Handle MkDocs Material instant navigation
  // The tabs DOM is preserved across instant navigation, so MutationObserver
  // watches for any tab re-renders
  new MutationObserver(function () {
    var hasTabs = document.querySelector(".md-tabs__link");
    var hasDropdown = document.querySelector(".tabs-dropdown");
    if (hasTabs && !hasDropdown) {
      buildDropdowns();
    }
  }).observe(document.documentElement, { childList: true, subtree: true });
})();
