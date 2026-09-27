# 16 - Android TV & Set-Top Box (Bilingual VI/EN)

Kiến thức phỏng vấn về phát triển Android TV và Set-Top Box (STB), bao gồm system-level, middleware, DRM, media pipeline, và hardware integration.

---

## 1) Android TV Architecture

### Q1. Android TV khác gì Android Mobile về architecture?

**A:**
- EN: Android TV is built on the same AOSP base but uses a lean-back UI (Leanback library), has no touchscreen input (D-pad/remote navigation), uses a different launcher (TV Home), and runs on lower-spec hardware (limited RAM/storage). It also enforces stricter background process management.
- VI: Android TV dùng cùng nền AOSP nhưng có giao diện lean-back (điều hướng bằng remote/D-pad), không có touchscreen, launcher riêng (TV Home), chạy trên hardware yếu hơn (RAM/storage hạn chế), và quản lý process nền chặt hơn.

Key differences:
- Input: D-pad navigation thay vì touch
- UI: Leanback support library (`BrowseSupportFragment`, `DetailsSupportFragment`)
- Resources: Thường 1-2GB RAM, hạn chế storage
- Display: Fixed landscape, overscan handling
- Audio: Passthrough (Dolby, DTS) qua HDMI

---

### Q2. Lean-back UI framework hoạt động thế nào?

**A:**
- EN: The Leanback library provides pre-built fragments optimized for TV: `BrowseSupportFragment` (content catalog), `DetailsSupportFragment` (item details), `SearchSupportFragment`, `PlaybackSupportFragment`. Navigation is focus-based using D-pad (up/down/left/right/select/back).
- VI: Leanback library cung cấp các fragment tối ưu cho TV. Navigation dựa trên focus thay vì touch.

```java
// BrowseFragment setup
public class MainFragment extends BrowseSupportFragment {
    @Override
    public void onActivityCreated(Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);
        setTitle("My STB App");
        setHeadersState(HEADERS_ENABLED);
        loadRows();  // populate with ArrayObjectAdapter
    }
}
```

Focus handling best practices:
- Đảm bảo mọi element có thể nhận focus
- Sử dụng `nextFocusDown/Up/Left/Right` cho navigation phức tạp
- Test với remote thật, không chỉ emulator

---

### Q3. TvInputFramework (TIF) là gì và vai trò trong STB?

**A:**
- EN: TIF is Android TV's framework for integrating live TV sources. It defines `TvInputService` (provides channel/program data), `TvContract` (content provider for EPG data), and `TvView` (renders TV content). STB manufacturers implement custom TvInputService to interface with tuners (DVB-T/S/C, ATSC, ISDB).
- VI: TIF là framework tích hợp nguồn TV trực tiếp. STB manufacturer implement `TvInputService` để giao tiếp với tuner hardware.

```
┌─────────────────────────────────────────┐
│            Live TV App (UI)             │
├─────────────────────────────────────────┤
│              TvView                      │
├─────────────────────────────────────────┤
│         TvInputManager                   │
├──────────────┬──────────────────────────┤
│ TvInputService│  TvInputService          │
│  (HDMI)      │  (DVB-T Tuner)           │
├──────────────┼──────────────────────────┤
│   HAL/Driver │  HAL/Driver              │
└──────────────┴──────────────────────────┘
```

---

## 2) Media Pipeline & Playback

### Q4. Media pipeline trên Android TV STB hoạt động thế nào?

**A:**
- EN: The pipeline typically flows: Source (network/tuner) → Demuxer (TS/MP4 parsing) → Decoder (hardware codec via MediaCodec) → Renderer (SurfaceView/TextureView for video, AudioTrack for audio). On STBs, hardware decoders are accessed through `MediaCodec` API backed by vendor-specific OMX/Codec2 implementations.
- VI: Pipeline: Source → Demux → Hardware Decoder (MediaCodec) → Render. STB dùng hardware codec thông qua OMX hoặc Codec2 HAL.

```
Network/Tuner → [Demux (TS)] → [Video Decoder (H.264/HEVC HW)]  → SurfaceView
                             → [Audio Decoder (AAC/AC3 HW)]     → AudioTrack
                             → [Subtitle Parser]                → Overlay
```

Key classes:
- `MediaCodec`: Hardware accelerated decode/encode
- `MediaExtractor`: Container demuxing
- `AudioTrack`: PCM output hoặc compressed passthrough
- `ExoPlayer`/`Media3`: High-level player thường dùng trong app

---

### Q5. ExoPlayer (Media3) trên STB cần lưu ý gì?

**A:**
- EN: On STBs, ExoPlayer must handle: limited buffer memory (reduce `DefaultLoadControl` buffer sizes), codec quirks (vendor-specific MediaCodec bugs), audio passthrough for surround sound (use `DefaultAudioSink` with passthrough mode), tunneled playback for A/V sync, and adaptive streaming with constrained bandwidth.
- VI: Trên STB cần điều chỉnh ExoPlayer: giảm buffer size, xử lý codec quirks, cấu hình audio passthrough, tunneled playback, và adaptive streaming.

```kotlin
val player = ExoPlayer.Builder(context)
    .setLoadControl(
        DefaultLoadControl.Builder()
            .setBufferDurationsMs(
                15_000,   // min buffer (giảm từ 50s mặc định)
                30_000,   // max buffer
                1_500,    // buffer for playback
                3_000     // buffer for rebuffer
            ).build()
    )
    .setRenderersFactory(DefaultRenderersFactory(context).apply {
        setEnableAudioTrackPlaybackParams(true)
        setExtensionRendererMode(EXTENSION_RENDERER_MODE_PREFER)
    })
    .build()
```

Tunneled playback (A/V sync tốt hơn cho live content):
```kotlin
val trackSelector = DefaultTrackSelector(context).apply {
    parameters = buildUponParameters()
        .setTunnelingEnabled(true)
        .build()
}
```

---

### Q6. Audio passthrough (Dolby Digital, DTS) hoạt động thế nào trên STB?

**A:**
- EN: Audio passthrough sends compressed bitstream directly to AVR/soundbar via HDMI without decoding on the STB. Android uses `AudioTrack` in `MODE_STATIC`/`MODE_STREAM` with `AudioFormat.ENCODING_AC3/E_AC3/DTS`. The HAL routes compressed data through HDMI ARC/eARC.
- VI: Audio passthrough gửi bitstream nén trực tiếp qua HDMI tới AVR mà không decode trên STB. Dùng `AudioTrack` với encoding tương ứng.

```java
// Check passthrough support
AudioManager am = getSystemService(AudioManager.class);
// API 23+
boolean ac3Supported = AudioTrack.isDirectPlaybackSupported(
    new AudioFormat.Builder()
        .setEncoding(AudioFormat.ENCODING_AC3)
        .setSampleRate(48000)
        .setChannelMask(AudioFormat.CHANNEL_OUT_5POINT1)
        .build(),
    new AudioAttributes.Builder()
        .setUsage(AudioAttributes.USAGE_MEDIA)
        .build()
);
```

Lưu ý:
- Phải check `isDirectPlaybackSupported` trước khi dùng passthrough
- Fallback về PCM decode nếu receiver không hỗ trợ
- HDMI hotplug có thể thay đổi capabilities → cần listen `AudioDeviceCallback`

---

## 3) DRM & Content Protection

### Q7. DRM trên Android TV STB triển khai thế nào?

**A:**
- EN: Android uses `MediaDrm` API as the framework interface. STBs typically support Widevine (L1 for HD/4K, requires TEE), PlayReady, and sometimes proprietary CAS. The security level depends on hardware: L1 requires Trusted Execution Environment (TEE/TrustZone) for key handling and decryption in secure memory.
- VI: Android dùng `MediaDrm` API. STB thường hỗ trợ Widevine L1 (cần TEE cho HD/4K), PlayReady. Security level phụ thuộc hardware TEE.

```
┌────────────────────────────────┐
│         App (ExoPlayer)        │
├────────────────────────────────┤
│     MediaDrm / MediaCrypto     │
├────────────────────────────────┤
│    DRM Plugin (Widevine CDM)   │
├────────────────────────────────┤
│   TEE (TrustZone / OP-TEE)    │  ← Keys never leave secure world
├────────────────────────────────┤
│   Secure Video Path (SVP)      │  ← Decrypted frames in secure memory
└────────────────────────────────┘
```

Widevine levels:
- L1: TEE decode + secure video path → 4K/HDR content
- L3: Software only → SD content, dễ bị crack

---

### Q8. CAS (Conditional Access System) khác DRM thế nào?

**A:**
- EN: CAS is for broadcast/linear TV (DVB, ISDB) - descrambles transport stream using smart card or software. DRM is for OTT/IP streaming - manages licenses for on-demand content. STBs often need both: CAS for live TV tuner input, DRM for streaming apps.
- VI: CAS dùng cho broadcast TV (descramble TS), DRM dùng cho OTT streaming. STB thường cần cả hai.

| | CAS | DRM |
|---|---|---|
| Use case | Live broadcast TV | OTT/VOD streaming |
| Transport | DVB TS (MPEG-2 TS) | DASH/HLS (MP4/fMP4) |
| Key delivery | EMM/ECM in TS | License server (HTTPS) |
| Hardware | Smart card / chipset | TEE / secure element |
| Examples | Nagra, Irdeto, Conax | Widevine, PlayReady |

Android TV integration:
- CAS: `MediaCas` API + `TvInputService` + Descrambler HAL
- DRM: `MediaDrm` + `MediaCrypto` + DRM HAL

---

## 4) System-Level & Hardware Integration

### Q9. Boot process của Android TV STB diễn ra thế nào?

**A:**
- EN: Boot sequence: Bootloader (vendor-specific, loads kernel) → Linux Kernel (device tree, drivers) → Init (init.rc, mounts partitions) → Zygote (forks app processes) → SystemServer (starts framework services) → TV Launcher. STBs add: secure boot chain verification, TEE initialization, and tuner/demux HAL startup.
- VI: Boot: Bootloader → Kernel → Init → Zygote → SystemServer → TV Launcher. STB thêm: secure boot, TEE init, tuner HAL.

```
[Bootloader] → verify signature → load kernel
    ↓
[Kernel] → device tree → load drivers (GPU, demux, tuner, HDMI)
    ↓
[Init] → mount partitions → start services (servicemanager, hwservicemanager)
    ↓
[Zygote] → preload classes/resources → fork SystemServer
    ↓
[SystemServer] → TvInputManagerService, MediaSessionService, ...
    ↓
[TV Launcher] → ready for user
```

Boot time optimization (quan trọng cho STB):
- Preload chỉ service cần thiết
- Defer non-critical services
- Kernel: strip unnecessary drivers, use compressed initramfs
- Target: < 15s cold boot (carrier requirement)

---

### Q10. HAL (Hardware Abstraction Layer) trong STB có những module nào quan trọng?

**A:**
- EN: Key HALs for STB: Tuner HAL (DVB demod control), Demux HAL (TS filtering/descrambling), CAS HAL (conditional access), Composer/HWC HAL (display compositing with video plane), Audio HAL (passthrough routing), HDMI-CEC HAL (remote control, device control), DRM HAL (content protection).
- VI: HAL quan trọng cho STB: Tuner, Demux, CAS, HWComposer, Audio, HDMI-CEC, DRM.

```
┌──────────────────────────────────────┐
│          Android Framework           │
├──────────────────────────────────────┤
│              HIDL / AIDL             │
├─────────┬────────┬────────┬──────────┤
│Tuner HAL│CAS HAL│Audio HAL│HDMI-CEC │
├─────────┼────────┼────────┼──────────┤
│ Vendor driver / kernel modules       │
├──────────────────────────────────────┤
│        SoC Hardware (Amlogic/        │
│        Realtek/MediaTek/HiSilicon)   │
└──────────────────────────────────────┘
```

Tuner HAL (Android 11+ AIDL-based):
- `IFrontend`: Control demodulator (DVB-T/S/C, ATSC, ISDB)
- `IDemux`: TS filtering, section filtering, PES extraction
- `IDescrambler`: CAS descrambling integration
- `IDvr`: Recording, timeshift buffer

---

### Q11. HDMI-CEC trên STB dùng để làm gì?

**A:**
- EN: HDMI-CEC (Consumer Electronics Control) allows devices on the same HDMI bus to control each other. On STB: one-touch play (STB turns on TV), system standby, volume control forwarding to AVR, active source switching. Android implements via `HdmiControlService` and `HdmiCecLocalDevice`.
- VI: HDMI-CEC cho phép STB điều khiển TV (bật/tắt, chuyển input, điều khiển volume). Android implement qua `HdmiControlService`.

Common CEC commands for STB:
- `<Image View On>`: Turn on TV display
- `<Active Source>`: Claim active input
- `<Standby>`: Put TV to sleep
- `<Set System Audio Mode>`: Route audio to AVR
- `<User Control Pressed>`: Forward remote key

```java
// Send CEC command from STB
HdmiControlManager hdmiControl = getSystemService(HdmiControlManager.class);
HdmiPlaybackClient client = hdmiControl.getPlaybackClient();
client.oneTouchPlay(new OneTouchPlayCallback() {
    @Override
    public void onComplete(int result) {
        // TV should now be on and showing STB input
    }
});
```

---

## 5) Performance & Memory Optimization

### Q12. STB thường có RAM hạn chế (1-2GB). Tối ưu memory thế nào?

**A:**
- EN: Key strategies: reduce app heap size (`largeHeap=false`), use `Bitmap.Config.RGB_565` for non-alpha images, release resources in `onStop`, use `LruCache` with strict limits, avoid memory leaks (static references to Context/View), use `android:process` to isolate heavy components, leverage `onTrimMemory()` callbacks.
- VI: Tối ưu RAM trên STB: giảm heap, dùng RGB_565, release tài nguyên sớm, tránh memory leak, tách process, xử lý `onTrimMemory`.

System-level optimizations:
```bash
# Trong build.prop hoặc device overlay
dalvik.vm.heapsize=128m
dalvik.vm.heapgrowthlimit=64m
ro.config.low_ram=true        # Enable low-RAM optimizations
config_lowMemoryKillerMinFreeKbytes=73728
```

App-level:
```kotlin
override fun onTrimMemory(level: Int) {
    when {
        level >= TRIM_MEMORY_COMPLETE -> clearAllCaches()
        level >= TRIM_MEMORY_MODERATE -> clearNonEssentialCaches()
        level >= TRIM_MEMORY_BACKGROUND -> clearImageCache()
    }
}
```

Monitoring:
- `adb shell dumpsys meminfo <package>` — app memory breakdown
- `adb shell cat /proc/meminfo` — system memory
- `adb shell dumpsys activity processes` — LMK priorities

---

### Q13. Làm sao đảm bảo smooth UI 60fps trên STB hardware yếu?

**A:**
- EN: Avoid overdraw (flat view hierarchy, use `ConstraintLayout`), reduce GPU work (simple backgrounds, avoid complex shadows), use `RecyclerView` with view recycling, preload/prefetch adjacent items, keep main thread < 16ms per frame, offload work to background threads, profile with `systrace`/Perfetto.
- VI: Giảm overdraw, flat hierarchy, RecyclerView với prefetch, giữ main thread < 16ms/frame, profile bằng systrace.

TV-specific tips:
- Focus animation phải lightweight (scale/alpha, không complex drawable)
- Image loading: downscale trước khi decode, dùng thumbnail
- Leanback `PresenterSelector`: reuse view holders tối đa
- Disable window animation nếu không cần (`windowAnimationStyle = null`)

```kotlin
// Prefetch cho horizontal scrolling
(recyclerView.layoutManager as LinearLayoutManager).apply {
    initialPrefetchItemCount = 4  // prefetch 4 items ahead
}
```

Profile:
```bash
adb shell atrace --async_start -c gfx view
# reproduce jank
adb shell atrace --async_stop > trace.txt
# Analyze with Perfetto UI
```

---

## 6) OTA Update & Device Management

### Q14. OTA update trên STB triển khai thế nào?

**A:**
- EN: STBs use A/B partition scheme (seamless update without downtime) or recovery-based update. The update flow: check server → download OTA package → verify signature → apply (streaming or block-based) → reboot to new slot. Rollback protection via verified boot + bootloader state.
- VI: STB dùng A/B partition (update không downtime) hoặc recovery. Flow: check → download → verify → apply → reboot. Có rollback protection.

```
Slot A (active)     Slot B (inactive)
┌──────────┐        ┌──────────┐
│  boot_a  │        │  boot_b  │  ← kernel + ramdisk
│ system_a │        │ system_b │  ← Android system
│ vendor_a │        │ vendor_b │  ← HAL implementations
└──────────┘        └──────────┘

OTA: write to inactive slot → mark as bootable → reboot
If boot fails → rollback to previous slot automatically
```

Key components:
- `UpdateEngine` (A/B): streaming update, background apply
- `RecoverySystem` (non-A/B): reboot to recovery partition
- Verified Boot (dm-verity): ensure partition integrity
- Carrier MDM: remote device management, force update policies

---

### Q15. Remote device management cho fleet STB gồm những gì?

**A:**
- EN: Fleet management for STBs includes: remote configuration (push settings/channel lists), telemetry collection (crash reports, usage analytics), remote diagnostics (logcat pull, screenshot), forced OTA updates, app provisioning (silent install/uninstall), and remote wipe/factory reset. Usually implemented via MQTT/CoAP for lightweight push.
- VI: Quản lý fleet STB: remote config, telemetry, diagnostics, force OTA, app provisioning, remote wipe. Thường dùng MQTT cho push.

Architecture:
```
┌─────────────────────────────────────┐
│      Device Management Server       │
│  (Config, OTA, Telemetry, Commands) │
└──────────────┬──────────────────────┘
               │ MQTT / HTTPS
┌──────────────▼──────────────────────┐
│        STB Device Agent             │
│  - Heartbeat / status report        │
│  - Execute remote commands          │
│  - Report crashes & ANR             │
│  - Apply config changes             │
│  - Trigger OTA                      │
└─────────────────────────────────────┘
```

---

## 7) Networking & Streaming Protocols

### Q16. Adaptive streaming (HLS/DASH) trên STB cần xử lý gì đặc biệt?

**A:**
- EN: STB considerations for adaptive streaming: bandwidth estimation with wired ethernet (more stable than mobile), buffer strategy for limited RAM, codec capability detection (not all STBs support HEVC/VP9/AV1), resolution capping based on HDMI output resolution, seamless quality switching without glitches on hardware decoders.
- VI: STB cần xử lý: bandwidth estimation (ethernet stable hơn), buffer giới hạn RAM, detect codec support, cap resolution theo HDMI output, seamless quality switch trên HW decoder.

Common issues on STB:
1. **Decoder reset on quality switch**: Một số SoC cần flush codec khi đổi resolution → đen màn hình
2. **Limited concurrent decoders**: Thường chỉ 1 video decoder → PiP cần SoC hỗ trợ
3. **Audio codec change**: Chuyển từ AAC sang AC3 mid-stream gây pop/gap

```kotlin
// Adaptive track selection giới hạn cho STB
val trackSelector = DefaultTrackSelector(context).apply {
    parameters = buildUponParameters()
        .setMaxVideoSize(1920, 1080)    // cap theo TV output
        .setPreferredAudioLanguage("vi")
        .setForceHighestSupportedBitrate(false)
        .build()
}
```

---

### Q17. Multicast/IPTV delivery trên STB thế nào?

**A:**
- EN: IPTV uses UDP multicast (IGMPv2/v3) for live channels. STB joins multicast group for the selected channel, leaves when changing. Requires: IGMP snooping on switches, multicast routing, join/leave latency < 500ms for acceptable channel zap time. Android doesn't natively support multicast well → vendor HAL or custom player needed.
- VI: IPTV dùng UDP multicast. STB join/leave group khi đổi kênh. Cần IGMP support, zap time < 500ms. Android không hỗ trợ tốt multicast → cần vendor HAL.

```
Headend                    Network              STB
┌──────┐    UDP Multicast   ┌──────┐    IGMP    ┌──────┐
│Source│ → 239.1.1.x:5000 → │Switch│ ← Join  ← │Device│
│(Live)│                    │(IGMP │            │      │
│      │                    │snoop)│            │Player│
└──────┘                    └──────┘            └──────┘
```

Channel zap optimization:
- Pre-join adjacent channels (predict user behavior)
- Use I-frame only stream for fast channel preview
- Buffer minimal amount before rendering first frame
- Dual-decoder: decode next channel while current plays

---

## 8) Testing & Debugging STB

### Q18. Debug Android TV STB khi không có màn hình (headless)?

**A:**
- EN: Use `adb` over network (`adb connect <ip>:5555`), `scrcpy` for screen mirroring, `adb shell screencap` for screenshots, `adb shell dumpsys` for service state, serial console (UART) for bootloader/kernel debug, JTAG for hardware-level debug on development boards.
- VI: Debug headless STB: adb qua network, scrcpy mirror, screencap, dumpsys, UART serial console, JTAG cho hardware debug.

Essential debug commands:
```bash
# Connect over network
adb connect 192.168.1.100:5555

# Screen capture
adb shell screencap /sdcard/screen.png && adb pull /sdcard/screen.png

# Check running services
adb shell dumpsys activity services | grep -i tuner

# Media codec info
adb shell dumpsys media.codec

# HDMI status
adb shell dumpsys display | grep -i hdmi

# Check thermal throttling
adb shell dumpsys thermalservice

# Memory pressure
adb shell dumpsys meminfo --summary
```

---

### Q19. CTS/VTS/GTS cho Android TV STB gồm những gì?

**A:**
- EN: CTS (Compatibility Test Suite) ensures API compatibility. VTS (Vendor Test Suite) tests HAL implementations. GTS (Google Test Suite) tests GMS requirements. For TV STB specifically: CTS-TV (TV-specific tests), media CTS (codec compliance), Widevine/PlayReady certification tests, carrier-specific acceptance tests.
- VI: CTS kiểm tra API compatibility, VTS kiểm tra HAL, GTS kiểm tra GMS. TV STB thêm: CTS-TV, media CTS, DRM certification, carrier acceptance test.

Test pyramid for STB:
```
        ┌─────────────────┐
        │ Carrier Acceptance│  ← Operator-specific tests
        ├─────────────────┤
        │   GTS / STS      │  ← Google services & security
        ├─────────────────┤
        │   CTS / CTS-TV   │  ← Android compatibility
        ├─────────────────┤
        │   VTS             │  ← HAL/driver compliance
        ├─────────────────┤
        │ Unit / Integration│  ← Developer tests
        └─────────────────┘
```

Critical CTS modules for STB:
- `CtsMediaTestCases`: Codec, DRM, playback
- `CtsTvTestCases`: TIF, EPG, channel
- `CtsSecurityTestCases`: SELinux, verified boot
- `CtsNetTestCases`: Ethernet, multicast

---

## 9) Common SoC Platforms

### Q20. Các SoC phổ biến cho Android TV STB và đặc điểm?

**A:**
- EN: Major STB SoCs: Amlogic (S905/S928 series - most popular, good price/performance), MediaTek (MT9xxx - mid-to-high range), HiSilicon (Hi3798 - Huawei ecosystem), Broadcom (BCM72xx - premium, cable operators), Realtek (RTD1xxx - cost-effective).
- VI: SoC phổ biến: Amlogic (phổ biến nhất, giá tốt), MediaTek (mid-high), HiSilicon (Huawei), Broadcom (premium), Realtek (giá rẻ).

| SoC | Series | Video Decode | Use Case |
|-----|--------|-------------|----------|
| Amlogic | S905X4/S928X | 4K HEVC, AV1, VP9 | Mid-range OTT box |
| MediaTek | MT9902 | 8K AV1, HEVC | Premium smart TV |
| HiSilicon | Hi3798MV310 | 4K HEVC, HDR | China market STB |
| Broadcom | BCM7218X | 4K HEVC, multi-decode | Cable/IPTV operator |
| Realtek | RTD1319D | 4K HEVC, VP9 | Budget OTT box |

Khi phỏng vấn, cần biết:
- BSP (Board Support Package) workflow: source → build → flash → test
- Vendor-specific bootloader (u-boot customized)
- GPU driver (Mali/PowerVR) và display pipeline
- Thermal design constraints (passive cooling)

---

## Flash Cards

| # | Question | Key Answer |
|---|----------|-----------|
| 1 | Android TV vs Mobile | Lean-back UI, D-pad nav, lower RAM, no touch |
| 2 | TIF | TvInputService + TvContract + TvView for live TV |
| 3 | Media pipeline | Source → Demux → HW Decoder (MediaCodec) → Render |
| 4 | Widevine L1 vs L3 | L1: TEE + secure video path (4K). L3: software only (SD) |
| 5 | CAS vs DRM | CAS: broadcast/TS. DRM: OTT/IP streaming |
| 6 | Audio passthrough | Compressed bitstream direct to AVR via HDMI |
| 7 | HDMI-CEC | Devices control each other on HDMI bus |
| 8 | A/B OTA | Dual partition, seamless update, auto rollback |
| 9 | IPTV multicast | UDP multicast + IGMP join/leave, zap < 500ms |
| 10 | STB SoCs | Amlogic (popular), MediaTek, Broadcom, Realtek |
