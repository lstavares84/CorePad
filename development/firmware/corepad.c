#include "corepad.h"
void cp_init(cp_state *s) {
    *s = (cp_state){.mode=CP_IDLE, .layer=1, .rgb={0,255,0}, .brightness=32};
}
void cp_authenticated(cp_state *s, bool trusted_result) {
    s->authenticated=trusted_result;
    if (!trusted_result && s->layer==3) s->layer=1;
}
bool cp_select_layer(cp_state *s, uint8_t layer) {
    if (layer<1 || layer>3 || (layer==3 && !s->authenticated)) return false;
    s->layer=layer; return true;
}
bool cp_start_recording(cp_state *s, bool card_ready) {
    if (s->mode!=CP_IDLE || !card_ready || s->battery_low) return false;
    s->mode=CP_RECORDING; return true;
}
bool cp_stop_recording(cp_state *s, bool synced) {
    if (s->mode!=CP_RECORDING) return false;
    s->mode=synced?CP_IDLE:CP_FAULT; return synced;
}
bool cp_enter_files(cp_state *s, bool unmounted) {
    if (s->mode!=CP_IDLE || !unmounted) return false;
    s->mode=CP_FILES; return true;
}
bool cp_leave_files(cp_state *s, bool ejected, bool mounted) {
    if (s->mode!=CP_FILES || !ejected) return false;
    s->mode=mounted?CP_IDLE:CP_FAULT; return mounted;
}
bool cp_low_battery(cp_state *s) {
    s->battery_low=true; s->rgb_enabled=false;
    cp_authenticated(s,false);
    return s->mode==CP_RECORDING;
}
void cp_set_rgb(cp_state *s, uint8_t r, uint8_t g, uint8_t b, uint8_t brightness, bool enabled) {
    s->rgb[0]=r; s->rgb[1]=g; s->rgb[2]=b; s->brightness=brightness;
    s->rgb_enabled=enabled && !s->battery_low;
}
