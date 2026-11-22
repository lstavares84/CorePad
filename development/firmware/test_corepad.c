#include "corepad.h"
#include <assert.h>
#include <stdio.h>
int main(void) {
    cp_state s; cp_init(&s);
    assert(!cp_select_layer(&s,3));
    assert(!cp_select_layer(&s,0));
    cp_authenticated(&s,true); assert(cp_select_layer(&s,3));
    cp_authenticated(&s,false); assert(s.layer==1);
    assert(!cp_enter_files(&s,false));
    assert(cp_enter_files(&s,true)); assert(!cp_start_recording(&s,true));
    assert(!cp_leave_files(&s,false,true)); assert(s.mode==CP_FILES);
    assert(cp_leave_files(&s,true,true));
    assert(!cp_start_recording(&s,false)); assert(cp_start_recording(&s,true));
    assert(!cp_enter_files(&s,true));
    cp_set_rgb(&s,1,2,3,255,true); assert(s.rgb_enabled);
    assert(cp_low_battery(&s)); assert(!s.rgb_enabled);
    assert(cp_stop_recording(&s,true)); assert(!cp_start_recording(&s,true));
    cp_init(&s); assert(cp_start_recording(&s,true));
    assert(!cp_stop_recording(&s,false)); assert(s.mode==CP_FAULT);
    cp_init(&s); assert(cp_enter_files(&s,true));
    assert(!cp_leave_files(&s,true,false)); assert(s.mode==CP_FAULT);
    puts("PASS: layer lock, card ownership, fault handling and low battery");
}
