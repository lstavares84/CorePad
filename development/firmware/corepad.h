#ifndef COREPAD_H
#define COREPAD_H
#include <stdbool.h>
#include <stdint.h>
typedef enum { CP_IDLE, CP_RECORDING, CP_FILES, CP_FAULT } cp_mode;
typedef struct {
    cp_mode mode;
    uint8_t layer, rgb[3], brightness;
    bool authenticated, rgb_enabled, battery_low;
} cp_state;
void cp_init(cp_state *s);
/* This assertion is supplied ONLY by a trusted authentication service, never by USB. */
void cp_authenticated(cp_state *s, bool trusted_result);
bool cp_select_layer(cp_state *s, uint8_t layer);
bool cp_start_recording(cp_state *s, bool card_ready);
bool cp_stop_recording(cp_state *s, bool file_closed_and_synced);
bool cp_enter_files(cp_state *s, bool local_fs_unmounted);
bool cp_leave_files(cp_state *s, bool host_ejected, bool local_fs_mounted);
/* Returns true when the audio/storage service must finalize an active recording. */
bool cp_low_battery(cp_state *s);
void cp_set_rgb(cp_state *s, uint8_t r, uint8_t g, uint8_t b, uint8_t brightness, bool enabled);
#endif
