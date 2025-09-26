# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.7] - 2025-09-26
### :bug: Bug Fixes
- [`8ec69a2`](https://github.com/jorben/etf-grid-design/commit/8ec69a2ca817f93ef7e132e4d7c0891d566956eb) - **analysis**: adjust volatility threshold criteria in suitability evaluation *(commit by [@jorben](https://github.com/jorben))*


## [0.1.6] - 2025-09-26
### :boom: BREAKING CHANGES
- due to [`45f0322`](https://github.com/jorben/etf-grid-design/commit/45f032222956b3ad11f13258ffa6232f588dd585) - restructure frontend application with modular architecture *(commit by [@jorben](https://github.com/jorben))*:

  Frontend application structure has been completely reorganized from monolithic to modular architecture. Import paths have changed to use alias-based imports (@shared, @features, @pages). Existing component references may need to be updated to use new module paths.

- due to [`1643e60`](https://github.com/jorben/etf-grid-design/commit/1643e60b30e496b5e887e80cc504d925455f4e14) - restructure project with modular architecture and path aliases *(commit by [@jorben](https://github.com/jorben))*:

  All component imports have been updated to use new path aliases. Existing relative imports will no longer work. Developers must update import statements to use @shared, @features, @pages, and @app aliases.

- due to [`53a6f0c`](https://github.com/jorben/etf-grid-design/commit/53a6f0c83500fae59afa3d66f28cbd333f23ba53) - restructure project with modular architecture and path aliases *(commit by [@jorben](https://github.com/jorben))*:

  项目目录结构发生重大变更，所有相对路径导入已更新为别名路径。需要更新开发环境配置以支持新的路径映射。


### :recycle: Refactors
- [`45f0322`](https://github.com/jorben/etf-grid-design/commit/45f032222956b3ad11f13258ffa6232f588dd585) - **frontend**: restructure frontend application with modular architecture *(commit by [@jorben](https://github.com/jorben))*
- [`1643e60`](https://github.com/jorben/etf-grid-design/commit/1643e60b30e496b5e887e80cc504d925455f4e14) - **frontend**: restructure project with modular architecture and path aliases *(commit by [@jorben](https://github.com/jorben))*
- [`53a6f0c`](https://github.com/jorben/etf-grid-design/commit/53a6f0c83500fae59afa3d66f28cbd333f23ba53) - **frontend**: restructure project with modular architecture and path aliases *(commit by [@jorben](https://github.com/jorben))*

### :wrench: Chores
- [`5019ad7`](https://github.com/jorben/etf-grid-design/commit/5019ad703890004236e1ac91be52e867593f7c37) - **release**: bump version to 0.1.6 *(commit by [@jorben](https://github.com/jorben))*


## [0.1.5] - 2025-09-25
### :sparkles: New Features
- [`43df8e9`](https://github.com/jorben/etf-grid-design/commit/43df8e91810d46204ce3b27d50be425e7850e4e4) - **report**: display latest price date in grid parameters card *(commit by [@jorben](https://github.com/jorben))*
- [`5c9674e`](https://github.com/jorben/etf-grid-design/commit/5c9674e77f15f60913c2256bdc67401ae802feaa) - use real-time price from Tushare for grid parameter calculation *(commit by [@jorben](https://github.com/jorben))*
- [`738add0`](https://github.com/jorben/etf-grid-design/commit/738add0fd9bee2ecc66fc491b35b93bd468387b9) - improve ETF name display format in analysis header *(commit by [@jorben](https://github.com/jorben))*

### :wrench: Chores
- [`fc9d44d`](https://github.com/jorben/etf-grid-design/commit/fc9d44dddb13439ef7a9cf1bfa81667ee06eed90) - bump version to 0.1.5 and add version-sync script *(commit by [@jorben](https://github.com/jorben))*


## [0.1.4] - 2025-09-25
### :bug: Bug Fixes
- [`15592e6`](https://github.com/jorben/etf-grid-design/commit/15592e66d0d5e818d63507c82aa805a1d3e8c971) - **ui**: append version to GitHub link label for clarity *(commit by [@jorben](https://github.com/jorben))*

### :recycle: Refactors
- [`5171c64`](https://github.com/jorben/etf-grid-design/commit/5171c6463f9e6de635ab5bdb1f36c0e70097ac53) - **grid**: switch from grid-count to fixed step-size for arithmetic & geometric grids *(commit by [@jorben](https://github.com/jorben))*

### :wrench: Chores
- [`cd236c3`](https://github.com/jorben/etf-grid-design/commit/cd236c3e9130ada52f1ab306bea83f79429fde1d) - bump version to 0.1.4 across all components *(commit by [@jorben](https://github.com/jorben))*


## [0.1.3] - 2025-09-25
### :sparkles: New Features
- [`7f0f512`](https://github.com/jorben/etf-grid-design/commit/7f0f512b2e002f913cce8cce7035eb96c15981f5) - centralize version management in config module *(commit by [@jorben](https://github.com/jorben))*

### :wrench: Chores
- [`1d536b4`](https://github.com/jorben/etf-grid-design/commit/1d536b43859ec9a68784c43ed8961cb7c0a5ade9) - bump version to 0.1.3 and add unified version updater script *(commit by [@jorben](https://github.com/jorben))*


## [0.1.2] - 2025-09-24
### :sparkles: New Features
- [`efd8940`](https://github.com/jorben/etf-grid-design/commit/efd894053b1ac3843ac49722229cb27263d4bef2) - restructure backend services and algorithms directories *(commit by [@jorben](https://github.com/jorben))*
- [`4e8f5fa`](https://github.com/jorben/etf-grid-design/commit/4e8f5fa10a4c72d68d36966c017209f0d3e71e40) - **api**: add middleware and refactor application structure *(commit by [@jorben](https://github.com/jorben))*
- [`5410cc4`](https://github.com/jorben/etf-grid-design/commit/5410cc471b747230ad0554b5c072f6e937e72be3) - extract ATR algorithms from service layer to dedicated module *(commit by [@jorben](https://github.com/jorben))*
- [`079cac3`](https://github.com/jorben/etf-grid-design/commit/079cac3d2e742caa69402f90c1c33912c6e6a658) - add configuration management module and update documentation *(commit by [@jorben](https://github.com/jorben))*
- [`f89d9ef`](https://github.com/jorben/etf-grid-design/commit/f89d9ef224ad1a4e8caf1e7ee5ffbd237a40327e) - add backend architecture documentation and update app configuration *(commit by [@jorben](https://github.com/jorben))*


## [0.1.1] - 2025-09-24
### :sparkles: New Features
- [`3a4f2cd`](https://github.com/jorben/etf-grid-design/commit/3a4f2cdd7a187c51dc2922cb786d82ca23dd40c1) - add global watermark component with responsive design *(commit by [@jorben](https://github.com/jorben))*


## [0.1.0] - 2025-09-24
### :sparkles: New Features
- [`6d98067`](https://github.com/jorben/etf-grid-design/commit/6d980673836476063c48c73eab401ec38c7f5b65) - add GitHub repository link to header navigation *(commit by [@jorben](https://github.com/jorben))*
- [`c65750d`](https://github.com/jorben/etf-grid-design/commit/c65750db7b77e17fd9f4a192e8a232169b6c14cc) - refactor ETF analysis system with comprehensive strategy framework *(commit by [@jorben](https://github.com/jorben))*
- [`3710a10`](https://github.com/jorben/etf-grid-design/commit/3710a1010cd28e6d2589e0c28aaed60f5ff79b27) - enhance ETF trading volume simulation and grid trading suitability analysis *(commit by [@jorben](https://github.com/jorben))*
- [`5161faf`](https://github.com/jorben/etf-grid-design/commit/5161fafe0567bb3865467e3cb5f82d667a6e1909) - require valid Tushare token and add environment configuration *(commit by [@jorben](https://github.com/jorben))*
- [`43b5364`](https://github.com/jorben/etf-grid-design/commit/43b53640f216955e9928d938f3b6e5e52f3db5b9) - **grid**: Optimize grid strategy fund allocation algorithm *(commit by [@jorben](https://github.com/jorben))*
- [`f464cbf`](https://github.com/jorben/etf-grid-design/commit/f464cbf8fa44a9142e6861b7accbca16342cbaf2) - **grid**: Implement ATR-based intelligent grid step strategy *(commit by [@jorben](https://github.com/jorben))*
- [`564813f`](https://github.com/jorben/etf-grid-design/commit/564813ffd54e8c76d9dbb19918ee2ce691c3f0c5) - **ui**: Optimize the display effect of suitability evaluation cards *(commit by [@jorben](https://github.com/jorben))*
- [`8386355`](https://github.com/jorben/etf-grid-design/commit/83863553d4f290ece776b7f41bf39a361ec14895) - **report**: Optimize Analysis Report Card Styles and Content *(commit by [@jorben](https://github.com/jorben))*
- [`1a97af9`](https://github.com/jorben/etf-grid-design/commit/1a97af9f68a6e138eb494edbc710cea197d2fcc6) - Optimize grid strategy display and add data quality evaluation module *(commit by [@jorben](https://github.com/jorben))*
- [`e9a8dc1`](https://github.com/jorben/etf-grid-design/commit/e9a8dc194fe51a86fb93ae270edb5d2b01b91248) - add ETF info skeleton loading component *(commit by [@jorben](https://github.com/jorben))*
- [`6f07c0e`](https://github.com/jorben/etf-grid-design/commit/6f07c0ee74b68bd4ae220c28e448fcf55eca8dc7) - **ui**: simplify ETF selection layout and reduce popular ETF list *(commit by [@jorben](https://github.com/jorben))*
- [`1c13ff9`](https://github.com/jorben/etf-grid-design/commit/1c13ff96c48c9169b09baafbc40e95cf9c4c39ba) - remove frequency preference parameter from ETF strategy analysis *(commit by [@jorben](https://github.com/jorben))*
- [`1e38b69`](https://github.com/jorben/etf-grid-design/commit/1e38b69c1131255b46437402f5a90826dc543933) - improve AnalysisReport UI layout and remove PDF export *(commit by [@jorben](https://github.com/jorben))*
- [`01a1500`](https://github.com/jorben/etf-grid-design/commit/01a1500812f7a3bee26bfeb7d48b57ca44b77b01) - add share functionality to AnalysisReport component *(commit by [@jorben](https://github.com/jorben))*
- [`55d6150`](https://github.com/jorben/etf-grid-design/commit/55d61503300cfb484a15061bc440be3a8dbc3135) - **frontend**: add react-helmet-async for SEO and meta tag management *(commit by [@jorben](https://github.com/jorben))*
- [`753fca3`](https://github.com/jorben/etf-grid-design/commit/753fca3afb2ab5bfa1917e2fb41d328cf03b8562) - **grid**: add base price anchoring to grid level calculation *(commit by [@jorben](https://github.com/jorben))*
- [`cdc0fc9`](https://github.com/jorben/etf-grid-design/commit/cdc0fc94f656d266eac2d07a23571f975e0c0d0a) - adjust ATR risk multipliers and grid strategy parameters *(commit by [@jorben](https://github.com/jorben))*
- [`5dddf4f`](https://github.com/jorben/etf-grid-design/commit/5dddf4ff20090d65a7e335b125fa9b45beabc921) - **grid**: improve buy grid calculation and price level display *(commit by [@jorben](https://github.com/jorben))*
- [`c5e9385`](https://github.com/jorben/etf-grid-design/commit/c5e9385a8bf26ac265d4192e1a8346c089d8318e) - **grid**: improve grid calculation with base price centering *(commit by [@jorben](https://github.com/jorben))*
- [`80ede6e`](https://github.com/jorben/etf-grid-design/commit/80ede6e1e58a29f62cc7ae5bc4dfb69eacca9882) - **ui**: add visual price range bar to GridParametersCard *(commit by [@jorben](https://github.com/jorben))*
- [`7ce7d20`](https://github.com/jorben/etf-grid-design/commit/7ce7d20ed01e3933141433821b0d28200c273e18) - refactor grid strategy display and move strategy analysis to dedicated component *(commit by [@jorben](https://github.com/jorben))*
- [`10aa58c`](https://github.com/jorben/etf-grid-design/commit/10aa58c65147528808fb570dfff39e36691ed726) - add version management system *(commit by [@jorben](https://github.com/jorben))*
- [`f7a960d`](https://github.com/jorben/etf-grid-design/commit/f7a960dd757dab6677e10c9c4ffd32f492192637) - **ui**: improve price range visualization in GridParametersCard *(commit by [@jorben](https://github.com/jorben))*
- [`7095a21`](https://github.com/jorben/etf-grid-design/commit/7095a21e4d3b06eaf8de5218c54e017a90ed762c) - add production static file serving and environment configuration *(commit by [@jorben](https://github.com/jorben))*

### :bug: Bug Fixes
- [`b552085`](https://github.com/jorben/etf-grid-design/commit/b55208510f17ac1f7603d00417d3318f0aa75338) - update screenshot URL to correct repository reference *(commit by [@jorben](https://github.com/jorben))*
- [`70728ff`](https://github.com/jorben/etf-grid-design/commit/70728ff3953577e3f56acf09256b7eca96f36e33) - correct screenshot filename typo in README *(commit by [@jorben](https://github.com/jorben))*

### :recycle: Refactors
- [`31b7e65`](https://github.com/jorben/etf-grid-design/commit/31b7e65d940bad415c4e37911c48e1e4c823e5dd) - **frontend**: Remove Recharts chart-related code *(commit by [@jorben](https://github.com/jorben))*
- [`e564a05`](https://github.com/jorben/etf-grid-design/commit/e564a05ba5de26012840443d36e6474efcd4ab65) - Unify terminology from "fitness" to "suitability" *(commit by [@jorben](https://github.com/jorben))*
- [`b3757b9`](https://github.com/jorben/etf-grid-design/commit/b3757b9dc4925a54a0123dd8df40976dce01d69f) - Remove ETF report summary feature *(commit by [@jorben](https://github.com/jorben))*
- [`4e4b6b6`](https://github.com/jorben/etf-grid-design/commit/4e4b6b6dacb842112ac6601a0d3ef6843cbf2ecc) - Remove preset configuration feature and optimize frontend UI *(commit by [@jorben](https://github.com/jorben))*
- [`62ca0fb`](https://github.com/jorben/etf-grid-design/commit/62ca0fbb7fda2403af8d64e8267bf800aa41a7c7) - remove hardcoded ETF data and update popular ETF list *(commit by [@jorben](https://github.com/jorben))*
- [`2523938`](https://github.com/jorben/etf-grid-design/commit/2523938c75ca8b8e839f060874da640af31b4d2e) - remove share functionality and restructure grid parameters display *(commit by [@jorben](https://github.com/jorben))*
- [`f32d985`](https://github.com/jorben/etf-grid-design/commit/f32d985324c9342a955b615d0121794fffd1e466) - improve grid trading quantity calculation for buy levels *(commit by [@jorben](https://github.com/jorben))*
- [`04d6125`](https://github.com/jorben/etf-grid-design/commit/04d6125b0f6b93674c8d52ed731efd2051cddb5a) - rename utilization_rate to grid_fund_utilization_rate *(commit by [@jorben](https://github.com/jorben))*
- [`15ef451`](https://github.com/jorben/etf-grid-design/commit/15ef45198778935cf88719151a0af5928785f74e) - remove backtest engine dependency from ETF analysis service *(commit by [@jorben](https://github.com/jorben))*
- [`726f216`](https://github.com/jorben/etf-grid-design/commit/726f2168f8edfca45821cc2745f24c80dedaf84a) - replace DataService with TushareClient for improved caching *(commit by [@jorben](https://github.com/jorben))*


## [0.0.3] - 2025-09-21
### :sparkles: New Features
- [`1e925fd`](https://github.com/jorben/etf-grid-design/commit/1e925fdf442bc832ff7e3bb2ce2a396f8efaf73d) - support URL query params for analysis page navigation *(commit by [@jorben](https://github.com/jorben))*

### :bug: Bug Fixes
- [`683ed56`](https://github.com/jorben/etf-grid-design/commit/683ed56c680b500a4c8ba46449857573ceee24c3) - update copyright text to include domain name *(commit by [@jorben](https://github.com/jorben))*


## [0.0.2] - 2025-09-21
### :sparkles: New Features
- [`acad14c`](https://github.com/jorben/etf-grid-design/commit/acad14ccf755802dd4d2c2c148d0e2ee6a3ac918) - Initialize ETF Grid Trading Strategy Design Tool project *(commit by [@jorben](https://github.com/jorben))*
- [`a192bc8`](https://github.com/jorben/etf-grid-design/commit/a192bc8691708096d81d2b92295bf487e0146058) - **etf**: add dimension scores to suitability analysis *(commit by [@jorben](https://github.com/jorben))*
- [`4652c9f`](https://github.com/jorben/etf-grid-design/commit/4652c9fd1f59908ac3a6473cb708795e30f61c0c) - **analysis**: enhance grid strategy with frequency matching and historical data *(commit by [@jorben](https://github.com/jorben))*
- [`52cca15`](https://github.com/jorben/etf-grid-design/commit/52cca15b476ab0c73bcb0b0a6edf369cf74fd4d7) - change backend port and refactor ETF grid trading evaluation *(commit by [@jorben](https://github.com/jorben))*
- [`ff5de28`](https://github.com/jorben/etf-grid-design/commit/ff5de28bda06d35ea7fd90519e4943b968193430) - Clean up test code *(commit by [@jorben](https://github.com/jorben))*
- [`5621aa1`](https://github.com/jorben/etf-grid-design/commit/5621aa1600d02cf95bd2d4b562fc363c9f9db73b) - **grid**: improve drawdown calculation and UI display formatting *(commit by [@jorben](https://github.com/jorben))*
- [`a3e38b9`](https://github.com/jorben/etf-grid-design/commit/a3e38b95b70df55da20b4cbf4bb8eba1d7584a3d) - implement dynamic shares calculator with target return optimization *(commit by [@jorben](https://github.com/jorben))*
- [`2477370`](https://github.com/jorben/etf-grid-design/commit/2477370c643bef9195bf26da21b80c6aaa290b3c) - add ETF name lookup API and optimize trading frequency parameters *(commit by [@jorben](https://github.com/jorben))*
- [`68e8a9e`](https://github.com/jorben/etf-grid-design/commit/68e8a9e201339bb995a929ac536016c03f91dbb3) - add file-based caching system with management endpoints *(commit by [@jorben](https://github.com/jorben))*
- [`bd2a307`](https://github.com/jorben/etf-grid-design/commit/bd2a307e3085061675cef5734ac9b3fab8835c14) - update UI text and icons for better user experience *(commit by [@jorben](https://github.com/jorben))*
- [`3bdd362`](https://github.com/jorben/etf-grid-design/commit/3bdd3628039cd0288607a8fa4e25a1084a775166) - add react-router-dom and implement page routing *(commit by [@jorben](https://github.com/jorben))*
- [`18a93fb`](https://github.com/jorben/etf-grid-design/commit/18a93fb69ca7f306524b4fff98e86357cd08ad68) - add Docker containerization support for ETF grid trading tool *(commit by [@jorben](https://github.com/jorben))*

### :bug: Bug Fixes
- [`62e5bdc`](https://github.com/jorben/etf-grid-design/commit/62e5bdc44d1ccb0c3b3db79c24c9594af4d349cd) - swap success/danger color semantics for price indicators *(commit by [@jorben](https://github.com/jorben))*

[0.0.2]: https://github.com/jorben/etf-grid-design/compare/0.0.1...0.0.2
[0.0.3]: https://github.com/jorben/etf-grid-design/compare/0.0.2...0.0.3
[0.1.0]: https://github.com/jorben/etf-grid-design/compare/0.0.3...0.1.0
[0.1.1]: https://github.com/jorben/etf-grid-design/compare/0.1.0...0.1.1
[0.1.2]: https://github.com/jorben/etf-grid-design/compare/0.1.1...0.1.2
[0.1.3]: https://github.com/jorben/etf-grid-design/compare/0.1.2...0.1.3
[0.1.4]: https://github.com/jorben/etf-grid-design/compare/0.1.3...0.1.4
[0.1.5]: https://github.com/jorben/etf-grid-design/compare/0.1.4...0.1.5
[0.1.6]: https://github.com/jorben/etf-grid-design/compare/0.1.5...0.1.6
[0.1.7]: https://github.com/jorben/etf-grid-design/compare/0.1.6...0.1.7
