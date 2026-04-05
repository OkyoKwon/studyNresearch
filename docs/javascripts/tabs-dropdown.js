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
      { label: "실물자산 토큰화 (RWA)", path: "domains/rwa/" },
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
    ],
    "부동산/투자": [
      { label: "부동산 투자", path: "domains/real-estate-investment/" },
      { label: "용인플랫폼시티", path: "domains/yongin-platform-city/" }
    ]
  };

  var portalMap = new WeakMap();
  var allDropdowns = [];
  var activeDropdown = null;
  var hideTimeout = null;

  function isDropdownsMapped() {
    var tabs = document.querySelectorAll(".md-tabs__link");
    for (var i = 0; i < tabs.length; i++) {
      var text = tabs[i].textContent.replace(/\s+/g, " ").trim();
      if (DROPDOWNS[text] && !portalMap.has(tabs[i].parentElement)) {
        return false;
      }
    }
    return allDropdowns.length > 0;
  }

  function findBaseUrl() {
    var tabs = document.querySelectorAll(".md-tabs__link");
    for (var i = 0; i < tabs.length; i++) {
      if (tabs[i].textContent.replace(/\s+/g, " ").trim() === "홈") {
        var a = document.createElement("a");
        a.href = tabs[i].getAttribute("href");
        var resolved = a.href;
        if (!resolved.endsWith("/")) resolved += "/";
        return resolved;
      }
    }
    if (typeof __md_scope !== "undefined") {
      return __md_scope.href;
    }
    return window.location.origin + "/";
  }

  function hideAllDropdowns() {
    clearTimeout(hideTimeout);
    allDropdowns.forEach(function (dd) {
      dd.style.display = "none";
    });
    activeDropdown = null;
  }

  function showDropdown(tabItem, dropdown) {
    clearTimeout(hideTimeout);
    hideAllDropdowns();

    var rect = tabItem.getBoundingClientRect();
    var left = rect.left;

    if (left + 240 > window.innerWidth) {
      left = window.innerWidth - 250;
    }
    if (left < 0) left = 4;

    dropdown.style.position = "fixed";
    dropdown.style.top = rect.bottom + "px";
    dropdown.style.left = left + "px";
    dropdown.style.display = "block";
    activeDropdown = dropdown;
  }

  function scheduleHide() {
    hideTimeout = setTimeout(function () {
      hideAllDropdowns();
    }, 150);
  }

  function cleanupPortals() {
    allDropdowns.forEach(function (dd) {
      if (dd.parentNode) {
        dd.parentNode.removeChild(dd);
      }
    });
    allDropdowns = [];
    activeDropdown = null;
    portalMap = new WeakMap();
  }

  function buildDropdowns() {
    var baseUrl = findBaseUrl();
    var tabs = document.querySelectorAll(".md-tabs__link");
    if (!tabs.length) return;

    tabs.forEach(function (tab) {
      var tabItem = tab.parentElement;
      if (portalMap.has(tabItem)) return;

      var text = tab.textContent.replace(/\s+/g, " ").trim();
      var items = DROPDOWNS[text];
      if (!items) return;

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

      document.body.appendChild(dropdown);
      portalMap.set(tabItem, dropdown);
      allDropdowns.push(dropdown);

      tabItem.addEventListener("mouseenter", function () {
        showDropdown(tabItem, dropdown);
      });

      tabItem.addEventListener("mouseleave", function () {
        scheduleHide();
      });

      dropdown.addEventListener("mouseenter", function () {
        clearTimeout(hideTimeout);
      });

      dropdown.addEventListener("mouseleave", function () {
        hideAllDropdowns();
      });
    });
  }

  function init() {
    buildDropdowns();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  window.addEventListener("load", init);

  window.addEventListener("scroll", function () {
    if (activeDropdown) {
      hideAllDropdowns();
    }
  }, { passive: true });

  new MutationObserver(function () {
    var hasTabs = document.querySelector(".md-tabs__link");
    if (hasTabs && !isDropdownsMapped()) {
      cleanupPortals();
      buildDropdowns();
    }
  }).observe(document.documentElement, { childList: true, subtree: true });
})();
