# This file is part of Xpra.
# Copyright (C) 2008, 2009 Nathaniel Smith <njs@pobox.com>
# Copyright (C) 2013-2019 Antoine Martin <antoine@xpra.org>
# Xpra is released under the terms of the GNU GPL v2, or, at your option, any
# later version. See the file COPYING for details.

import binascii
import traceback
import threading
import sys
import os
import re


XPRA_APP_ID = 0

XPRA_GUID1 = 0x67b3efa2
XPRA_GUID2 = 0xe470
XPRA_GUID3 = 0x4a5f
XPRA_GUID4 = (0xb6, 0x53, 0x6f, 0x6f, 0x98, 0xfe, 0x60, 0x81)
XPRA_GUID_STR = "67B3EFA2-E470-4A5F-B653-6F6F98FE6081"
XPRA_GUID_BYTES = binascii.unhexlify(XPRA_GUID_STR.replace("-",""))


XPRA_NOTIFICATIONS_OFFSET = 2**24
XPRA_BANDWIDTH_NOTIFICATION_ID  = XPRA_NOTIFICATIONS_OFFSET+1
XPRA_IDLE_NOTIFICATION_ID       = XPRA_NOTIFICATIONS_OFFSET+2
XPRA_WEBCAM_NOTIFICATION_ID     = XPRA_NOTIFICATIONS_OFFSET+3
XPRA_AUDIO_NOTIFICATION_ID      = XPRA_NOTIFICATIONS_OFFSET+4
XPRA_OPENGL_NOTIFICATION_ID     = XPRA_NOTIFICATIONS_OFFSET+5
XPRA_SCALING_NOTIFICATION_ID    = XPRA_NOTIFICATIONS_OFFSET+6
XPRA_NEW_USER_NOTIFICATION_ID   = XPRA_NOTIFICATIONS_OFFSET+7
XPRA_CLIPBOARD_NOTIFICATION_ID  = XPRA_NOTIFICATIONS_OFFSET+8
XPRA_FAILURE_NOTIFICATION_ID    = XPRA_NOTIFICATIONS_OFFSET+9
XPRA_DPI_NOTIFICATION_ID        = XPRA_NOTIFICATIONS_OFFSET+10
XPRA_DISCONNECT_NOTIFICATION_ID = XPRA_NOTIFICATIONS_OFFSET+11


#constants shared between client and server:
#(do not modify the values, see also disconnect_is_an_error)
#timeouts:
CLIENT_PING_TIMEOUT     = "client ping timeout"
LOGIN_TIMEOUT           = "login timeout"
CLIENT_EXIT_TIMEOUT     = "client exit timeout"
#errors:
PROTOCOL_ERROR          = "protocol error"
VERSION_ERROR           = "version error"
CONTROL_COMMAND_ERROR   = "control command error"
AUTHENTICATION_ERROR    = "authentication error"
PERMISSION_ERROR        = "permission error"
SERVER_ERROR            = "server error"
SESSION_NOT_FOUND       = "session not found error"
#informational (not a problem):
DONE                    = "done"
SERVER_EXIT             = "server exit"
SERVER_UPGRADE          = "server upgrade"
SERVER_SHUTDOWN         = "server shutdown"
CLIENT_REQUEST          = "client request"
DETACH_REQUEST          = "detach request"
NEW_CLIENT              = "new client"
IDLE_TIMEOUT            = "idle timeout"
SESSION_BUSY            = "session busy"
#client telling the server:
CLIENT_EXIT             = "client exit"


DEFAULT_PORT = 14500

DEFAULT_PORTS = {
    "ws"    : 80,
    "wss"   : 443,
    "ssh"   : 22,
    "tcp"   : DEFAULT_PORT,
    "udp"   : DEFAULT_PORT,
    }


#magic value for "workspace" window property, means unset
WORKSPACE_UNSET = 65535
WORKSPACE_ALL = 0xffffffff

WORKSPACE_NAMES = {
                   WORKSPACE_UNSET  : "unset",
                   WORKSPACE_ALL    : "all",
                   }

#this default value is based on 0.14.19 clients,
#later clients should provide the 'metadata.supported" capability instead
DEFAULT_METADATA_SUPPORTED = ("title", "icon-title", "pid", "iconic",
                              "size-hints", "class-instance", "client-machine",
                              "transient-for", "window-type",
                              "fullscreen", "maximized", "decorations", "skip-taskbar", "skip-pager",
                              "has-alpha", "override-redirect", "tray", "modal",
                              "role", "opacity", "xid", "group-leader")


#initiate-moveresize X11 constants
MOVERESIZE_SIZE_TOPLEFT      = 0
MOVERESIZE_SIZE_TOP          = 1
MOVERESIZE_SIZE_TOPRIGHT     = 2
MOVERESIZE_SIZE_RIGHT        = 3
MOVERESIZE_SIZE_BOTTOMRIGHT  = 4
MOVERESIZE_SIZE_BOTTOM       = 5
MOVERESIZE_SIZE_BOTTOMLEFT   = 6
MOVERESIZE_SIZE_LEFT         = 7
MOVERESIZE_MOVE              = 8
MOVERESIZE_SIZE_KEYBOARD     = 9
MOVERESIZE_MOVE_KEYBOARD     = 10
MOVERESIZE_CANCEL            = 11
MOVERESIZE_DIRECTION_STRING = {
                               MOVERESIZE_SIZE_TOPLEFT      : "SIZE_TOPLEFT",
                               MOVERESIZE_SIZE_TOP          : "SIZE_TOP",
                               MOVERESIZE_SIZE_TOPRIGHT     : "SIZE_TOPRIGHT",
                               MOVERESIZE_SIZE_RIGHT        : "SIZE_RIGHT",
                               MOVERESIZE_SIZE_BOTTOMRIGHT  : "SIZE_BOTTOMRIGHT",
                               MOVERESIZE_SIZE_BOTTOM       : "SIZE_BOTTOM",
                               MOVERESIZE_SIZE_BOTTOMLEFT   : "SIZE_BOTTOMLEFT",
                               MOVERESIZE_SIZE_LEFT         : "SIZE_LEFT",
                               MOVERESIZE_MOVE              : "MOVE",
                               MOVERESIZE_SIZE_KEYBOARD     : "SIZE_KEYBOARD",
                               MOVERESIZE_MOVE_KEYBOARD     : "MOVE_KEYBOARD",
                               MOVERESIZE_CANCEL            : "CANCEL",
                               }
SOURCE_INDICATION_UNSET     = 0
SOURCE_INDICATION_NORMAL    = 1
SOURCE_INDICATION_PAGER     = 2
SOURCE_INDICATION_STRING    = {
                               SOURCE_INDICATION_UNSET      : "UNSET",
                               SOURCE_INDICATION_NORMAL     : "NORMAL",
                               SOURCE_INDICATION_PAGER      : "PAGER",
                               }


util_logger = None
def get_util_logger():
    global util_logger
    if not util_logger:
        from xpra.log import Logger
        util_logger = Logger("util")
    return util_logger


#convenience method based on the strings above:
def disconnect_is_an_error(reason):
    return reason.find("error")>=0 or (reason.find("timeout")>=0 and reason!=IDLE_TIMEOUT)


if sys.version > '3':
    unicode = str           #@ReservedAssignment


def dump_exc():
    """Call this from a except: clause to print a nice traceback."""
    print("".join(traceback.format_exception(*sys.exc_info())))

# A simple little class whose instances we can stick random bags of attributes
# on.
class AdHocStruct(object):
    def __repr__(self):
        return ("<%s object, contents: %r>"
                % (type(self).__name__, self.__dict__))


def remove_dupes(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def merge_dicts(a, b, path=None):
    """ merges b into a """
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_dicts(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a

def make_instance(class_options, *args):
    log = get_util_logger()
    log("make_instance%s", tuple([class_options]+list(args)))
    for c in class_options:
        if c is None:
            continue
        try:
            v = c(*args)
            log("make_instance(..) %s()=%s", c, v)
            if v:
                return v
        except Exception:
            log.error("make_instance(%s, %s)", class_options, args, exc_info=True)
            log.error("Error: cannot instantiate %s:", c)
            log.error(" with arguments %s", tuple(args))
    return None


def roundup(n, m):
    return (n + m - 1) & ~(m - 1)


class AtomicInteger(object):
    def __init__(self, integer = 0):
        self.counter = integer
        self.lock = threading.RLock()

    def increase(self, inc = 1):
        with self.lock:
            self.counter = self.counter + inc
            return self.counter

    def decrease(self, dec = 1):
        with self.lock:
            self.counter = self.counter - dec
            return self.counter

    def get(self):
        return self.counter

    def __str__(self):
        return str(self.counter)

    def __repr__(self):
        return "AtomicInteger(%s)" % self.counter


    def __int__(self):
        return self.counter

    def __eq__(self, other):
        try:
            return self.counter==int(other)
        except ValueError:
            return -1

    def __cmp__(self, other):
        try:
            return self.counter-int(other)
        except ValueError:
            return -1


class MutableInteger(object):
    def __init__(self, integer = 0):
        self.counter = integer

    def increase(self, inc = 1):
        self.counter = self.counter + inc
        return self.counter

    def decrease(self, dec = 1):
        self.counter = self.counter - dec
        return self.counter

    def get(self):
        return self.counter

    def __str__(self):
        return str(self.counter)

    def __repr__(self):
        return "MutableInteger(%s)" % self.counter


    def __int__(self):
        return self.counter

    def __eq__(self, other):
        return self.counter==int(other)
    def __ne__(self, other):
        return self.counter!=int(other)
    def __lt__(self, other):
        return self.counter<int(other)
    def __le__(self, other):
        return self.counter<=int(other)
    def __gt__(self, other):
        return self.counter>int(other)
    def __ge__(self, other):
        return self.counter>=int(other)
    def __cmp__(self, other):
        return self.counter-int(other)


class typedict(dict):

    def _warn(self, msg, *args, **kwargs):
        get_util_logger().warn(msg, *args, **kwargs)

    def rawget(self, key, default=None):
        v = self.get(key)
        #py3k and bytes as keys...
        if v is None and isinstance(key, str):
            from xpra.os_util import strtobytes
            v = self.get(strtobytes(key), default)
        return v

    def capsget(self, key, default=None):
        v = self.rawget(key, default)
        if sys.version >= '3' and isinstance(v, bytes):
            from xpra.os_util import bytestostr
            v = bytestostr(v)
        return v

    def strget(self, k, default=None):
        v = self.capsget(k, default)
        if v is None:
            return default
        from xpra.os_util import bytestostr
        return bytestostr(v)

    def bytesget(self, k, default=None):
        v = self.capsget(k, default)
        if v is None:
            return default
        from xpra.os_util import strtobytes
        return strtobytes(v)

    def intget(self, k, d=0):
        v = self.capsget(k)
        if v is None:
            return d
        try:
            return int(v)
        except Exception as e:
            self._warn("intget(%s, %s)", k, d, exc_info=True)
            self._warn("Warning: failed to parse %s value '%s':", k, v)
            self._warn(" %s", e)
            return d

    def boolget(self, k, default_value=False):
        v = self.capsget(k)
        if v is None:
            return default_value
        return bool(v)

    def dictget(self, k, default_value=None):
        v = self.capsget(k, default_value)
        if v is None:
            return default_value
        if not isinstance(v, dict):
            self._warn("dictget(%s, %s)", k, default_value)
            self._warn("Warning: expected a dict value for %s but got %s", k, type(v))
            return default_value
        return v

    def intpair(self, k, default_value=None):
        v = self.intlistget(k, default_value)
        if v is None:
            return default_value
        if len(v)!=2:
            #"%s is not a pair of numbers: %s" % (k, len(v))
            return default_value
        try:
            return int(v[0]), int(v[1])
        except ValueError:
            return default_value

    def strlistget(self, k, default_value=[], min_items=None, max_items=None):
        return self.listget(k, default_value, str, min_items, max_items)

    def intlistget(self, k, default_value=[], min_items=None, max_items=None):
        return self.listget(k, default_value, int, min_items, max_items)

    def listget(self, k, default_value=[], item_type=None, min_items=None, max_items=None):
        v = self.capsget(k)
        if v is None:
            return default_value
        if not isinstance(v, (list, tuple)):
            self._warn("listget%s", (k, default_value, item_type, max_items))
            self._warn("expected a list or tuple value for %s but got %s", k, type(v))
            return default_value
        if min_items is not None:
            if len(v)<min_items:
                self._warn("too few items in %s %s: minimum %s allowed, but got %s", type(v), k, max_items, len(v))
                return default_value
        if max_items is not None:
            if len(v)>max_items:
                self._warn("too many items in %s %s: maximum %s allowed, but got %s", type(v), k, max_items, len(v))
                return default_value
        aslist = list(v)
        if item_type:
            for i, x in enumerate(aslist):
                if sys.version_info[0]>=3 and isinstance(x, bytes) and item_type==str:
                    from xpra.os_util import bytestostr
                    x = bytestostr(x)
                    aslist[i] = x
                elif isinstance(x, unicode) and item_type==str:
                    x = str(x)
                    aslist[i] = x
                if not isinstance(x, item_type):
                    self._warn("invalid item type for %s %s: expected %s but got %s", type(v), k, item_type, type(x))
                    return default_value
        return aslist


def parse_scaling_value(v):
    if not v:
        return None
    values = v.replace("/", ":").replace(",", ":").split(":", 1)
    values = [int(x) for x in values]
    for x in values:
        assert x>0, "invalid scaling value %s" % x
    if len(values)==1:
        ret = 1, values[0]
    else:
        assert values[0]<=values[1], "cannot upscale"
        ret = values[0], values[1]
    return ret

def from0to100(v):
    return intrangevalidator(v, 0, 100)

def intrangevalidator(v, min_value=None, max_value=None):
    v = int(v)
    if min_value is not None and v<min_value:
        raise ValueError("value must be greater than %i" % min_value)
    if max_value is not None and v>max_value:
        raise ValueError("value must be lower than %i" % max_value)
    return v


def log_screen_sizes(root_w, root_h, sizes):
    try:
        do_log_screen_sizes(root_w, root_h, sizes)
    except Exception as e:
        get_util_logger().warn("failed to parse screen size information: %s", e, exc_info=True)

def prettify_plug_name(s, default=""):
    if not s:
        return default
    try:
        s = s.decode("utf8")
    except (AttributeError, UnicodeDecodeError):
        pass
    #prettify strings on win32
    s = re.sub(r"[0-9\.]*\\", "-", s).lstrip("-")
    if s.startswith("WinSta-"):
        s = s[len("WinSta-"):]
    if s=="0":
        s = default
    return s

def do_log_screen_sizes(root_w, root_h, sizes):
    log = get_util_logger()
    #old format, used by some clients (android):
    if not isinstance(sizes, (tuple, list)):
        return
    if any(True for x in sizes if not isinstance(x, (tuple, list))):
        return
    def dpi(size_pixels, size_mm):
        if size_mm==0:
            return 0
        return int(size_pixels * 254 / size_mm / 10)
    for s in sizes:
        if len(s)<10:
            log.info(" %s", s)
            continue
        #more detailed output:
        display_name, width, height, width_mm, height_mm, \
        monitors, work_x, work_y, work_width, work_height = s[:10]
        #always log plug name:
        info = ["%s" % prettify_plug_name(display_name)]
        if width!=root_w or height!=root_h:
            #log plug dimensions if not the same as display (root):
            info.append("%ix%i" % (width, height))
        info.append("(%ix%i mm - DPI: %ix%i)" % (width_mm, height_mm, dpi(width, width_mm), dpi(height, height_mm)))
        def add_workarea(wx, wy, ww, wh):
            info.append("workarea: %ix%i" % (ww, wh))
            if wx!=0 or wy!=0:
                #log position if not (0, 0)
                info.append("at %ix%i" % (wx, wy))

        if work_width!=width or work_height!=height or work_x!=0 or work_y!=0:
            add_workarea(work_x, work_y, work_width, work_height)
        log.info("  "+" ".join(info))
        for i, m in enumerate(monitors, start=1):
            if len(m)<7:
                log.info("    %s", m)
                continue
            plug_name, plug_x, plug_y, plug_width, plug_height, plug_width_mm, plug_height_mm = m[:7]
            info = ['%s' % prettify_plug_name(plug_name, "monitor %i" % (i+1))]
            if plug_width!=width or plug_height!=height or plug_x!=0 or plug_y!=0:
                info.append("%ix%i" % (plug_width, plug_height))
                if plug_x!=0 or plug_y!=0:
                    info.append("at %ix%i" % (plug_x, plug_y))
            if (plug_width_mm!=width_mm or plug_height_mm!=height_mm) and (plug_width_mm>0 or plug_height_mm>0):
                info.append("(%ix%i mm - DPI: %ix%i)" % (
                    plug_width_mm, plug_height_mm, dpi(plug_width, plug_width_mm), dpi(plug_height, plug_height_mm))
                )
            if len(m)>=11:
                dwork_x, dwork_y, dwork_width, dwork_height = m[7:11]
                #only show it again if different from the screen workarea
                if dwork_x!=work_x or dwork_y!=work_y or dwork_width!=work_width or dwork_height!=work_height:
                    add_workarea(dwork_x, dwork_y, dwork_width, dwork_height)
            log.info("    "+" ".join(info))

def get_screen_info(screen_sizes):
    #same format as above
    if not screen_sizes:
        return {}
    info = {
            "screens" : len(screen_sizes)
            }
    for i, x in enumerate(screen_sizes):
        if not isinstance(x, (tuple, list)):
            continue
        sinfo = info.setdefault("screen", {}).setdefault(i, {})
        sinfo["display"] = x[0]
        if len(x)>=3:
            sinfo["size"] = x[1], x[2]
        if len(x)>=5:
            sinfo["size_mm"] = x[3], x[4]
        if len(x)>=6:
            monitors = x[5]
            for j, monitor in enumerate(monitors):
                if len(monitor)>=7:
                    minfo = sinfo.setdefault("monitor", {}).setdefault(j, {})
                    for k,v in {
                                "name"      : monitor[0],
                                "geometry"  : monitor[1:5],
                                "size_mm"   : monitor[5:7],
                                }.items():
                        minfo[k] = v
        if len(x)>=10:
            sinfo["workarea"] = x[6:10]
    return info

def dump_all_frames(logger=None):
    try:
        frames = sys._current_frames()
    except AttributeError:
        return
    else:
        dump_frames(frames.items(), logger)

def dump_gc_frames(logger=None):
    import gc
    #import types
    import inspect
    gc.collect()
    #frames = tuple(x for x in gc.get_objects() if isinstance(x, types.FrameType))
    frames = tuple((None, x) for x in gc.get_objects() if inspect.isframe(x))
    dump_frames(frames, logger)

def dump_frames(frames, logger=None):
    if not logger:
        logger = get_util_logger()
    logger("found %s frames:", len(frames))
    for i,(fid,frame) in enumerate(frames):
        fidstr = ""
        if fid is not None:
            try:
                fidstr = hex(fid)
            except TypeError:
                fidstr = str(fid)
        logger("%i: %s %s:", i, fidstr, frame)
        for x in traceback.format_stack(frame):
            for l in x.splitlines():
                logger("%s", l)


def dump_references(log, instances, exclude=[]):
    import gc
    import inspect
    frame = inspect.currentframe()
    exclude.append(instances)
    exclude.append([frame])
    exclude = [[frame],]
    rexclude = exclude
    np = sys.modules.get("numpy")
    if np:
        rexclude = []
        skip_types = (np.ndarray, np.generic)
        for v in exclude:
            rexclude.append(tuple(x for x in v if not isinstance(x, skip_types)))
    del exclude
    gc.collect()
    try:
        log.info("dump references for %i instances:", len(instances))
        for j, instance in enumerate(instances):
            referrers = tuple(x for x in gc.get_referrers(instance) if not any(y for y in rexclude if x in y))
            log.info("* %i : %s, type=%s, with %i referers",
                     j, repr_ellipsized(str(instance)), type(instance), len(referrers))
            j += 1
            for i, r in enumerate(referrers):
                log.info("  [%s] in %s", i, type(r))
                if inspect.isframe(r):
                    log.info("    frame info: %s", str(inspect.getframeinfo(r))[:1024])
                elif isinstance(r, (list, tuple)):
                    listref = gc.get_referrers(r)
                    lr = len(r)
                    if lr<=128:
                        log.info("    %i %s items: %s", lr, type(r), csv(repr_ellipsized(str(x)) for x in r))
                    elif lr<512:
                        log.info("    %i %s items: %s..", lr, type(r), repr_ellipsized(csv(r)))
                    else:
                        log.info("    %i %s items", lr, type(r))
                    ll = len(listref)
                    if ll<128:
                        log.info("    %i referrers: %s", ll, csv(repr_ellipsized(str(x)) for x in listref))
                    elif ll<512:
                        log.info("    %i referrers: %s", ll, repr_ellipsized(csv(listref)))
                    else:
                        log.info("    %i referrers", ll)
                elif isinstance(r, dict):
                    if len(r)>64:
                        log.info("    %s items: %s", len(r), repr_ellipsized(str(r)))
                        continue
                    for k,v in r.items():
                        if k is instance:
                            log.info("    key with value=%s", repr_ellipsized(str(v)))
                        elif v is instance:
                            log.info("    for key=%s", repr_ellipsized(str(k)))
                else:
                    log.info("     %s", repr_ellipsized(str(r)))
    finally:
        del frame

def detect_leaks():
    try:
        from pympler import tracker
    except ImportError as e:
        get_util_logger().warn("Warning: cannot enable memory leak detection:")
        get_util_logger().warn(" %s", e)
        return None
    import gc
    gc.enable()
    gc.set_debug(gc.DEBUG_LEAK)
    tr = tracker.SummaryTracker()
    def print_leaks():
        tr.print_diff()
        return True
    return print_leaks

def start_mem_watcher(ms):
    from xpra.make_thread import start_thread
    start_thread(mem_watcher, name="mem-watcher", daemon=True, args=(ms,))

def mem_watcher(ms, pid=os.getpid()):
    import time
    import psutil
    process = psutil.Process(pid)
    while True:
        mem = process.memory_full_info()
        #get_util_logger().info("memory usage: %s", mem.mem//1024//1024)
        get_util_logger().info("memory usage for %s: %s", pid, mem)
        time.sleep(ms/1000.0)

def log_mem_info(prefix="memory usage: ", pid=os.getpid()):
    import psutil
    process = psutil.Process(pid)
    mem = process.memory_full_info()
    print("%i %s%s" % (pid, prefix, mem))


def repr_ellipsized(obj, limit=100):
    if isinstance(obj, (str, unicode)) and len(obj) > limit:
        try:
            s = repr(obj)
        except ValueError:
            s = binascii.hexlify(obj)
        if len(s)<=limit or limit<=6:
            return s
        return s[:limit//2-2]+" .. "+s[2-limit//2:]
    return repr(obj)


def rindex(alist, avalue):
    return len(alist) - alist[::-1].index(avalue) - 1

def iround(v):
    return int(v+0.5)


def notypedict(d):
    for k in list(d.keys()):
        v = d[k]
        if isinstance(v, dict):
            d[k] = notypedict(v)
    return dict(d)

def flatten_dict(info, sep="."):
    to = {}
    _flatten_dict(to, sep, None, info)
    return to

def _flatten_dict(to, sep, path, d):
    from xpra.os_util import bytestostr
    for k,v in d.items():
        if path:
            if k:
                npath = path+sep+bytestostr(k)
            else:
                npath = path
        else:
            npath = bytestostr(k)
        if isinstance(v, dict):
            _flatten_dict(to, sep, npath, v)
        elif v is not None:
            to[npath] = v

def parse_simple_dict(s="", sep=","):
    #parse the options string and add the pairs:
    d = {}
    for el in s.split(sep):
        if not el:
            continue
        try:
            k,v = el.split("=", 1)
            d[k] = v
        except Exception as e:
            log = get_util_logger()
            log.warn("Warning: failed to parse dictionary option '%s':", s)
            log.warn(" %s", e)
    return d

#used for merging dicts with a prefix and suffix
#non-None values get added to <todict> with a prefix and optional suffix
def updict(todict, prefix, d, suffix="", flatten_dicts=False):
    if not d:
        return todict
    for k,v in d.items():
        if v is not None:
            if k:
                k = prefix+"."+str(k)
            else:
                k = prefix
            if suffix:
                k = k+"."+suffix
            if flatten_dicts and isinstance(v, dict):
                updict(todict, k, v)
            else:
                todict[k] = v
    return todict

def pver(v, numsep=".", strsep=", "):
    #print for lists with version numbers, or CSV strings
    if isinstance(v, (list, tuple)):
        types = list(set(type(x) for x in v))
        if len(types)==1 and types[0]==int:
            return numsep.join(str(x) for x in v)
        if len(types)==1 and types[0] in (str, unicode):
            return strsep.join(str(x) for x in v)
    from xpra.os_util import bytestostr
    return bytestostr(v)

def sorted_nicely(l):
    """ Sort the given iterable in the way that humans expect."""
    def convert(text):
        if text.isdigit():
            return int(text)
        return text
    from xpra.os_util import bytestostr
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', bytestostr(key))]
    return sorted(l, key = alphanum_key)

def print_nested_dict(d, prefix="", lchar="*", pad=32, vformat=None, print_fn=None,
                      version_keys=("version", "revision"), hex_keys=("data", )):
    #"smart" value formatting function:
    def sprint(arg):
        if print_fn:
            print_fn(arg)
        else:
            print(arg)
    def vf(k, v):
        if vformat:
            fmt = vformat
            if isinstance(vformat, dict):
                fmt = vformat.get(k)
            if fmt is not None:
                return nonl(fmt(v))
        try:
            if any(k.find(x)>=0 for x in version_keys):
                return nonl(pver(v)).lstrip("v")
            if any(k.find(x)>=0 for x in hex_keys):
                return binascii.hexlify(v)
        except Exception:
            pass
        return nonl(pver(v, ", ", ", "))
    l = pad-len(prefix)-len(lchar)
    from xpra.os_util import bytestostr
    for k in sorted_nicely(d.keys()):
        v = d[k]
        if isinstance(v, dict):
            nokey = v.get("", (v.get(None)))
            if nokey is not None:
                sprint("%s%s %s : %s" % (prefix, lchar, bytestostr(k).ljust(l), vf(k, nokey)))
                for x in ("", None):
                    try:
                        del v[x]
                    except KeyError:
                        pass
            else:
                sprint("%s%s %s" % (prefix, lchar, bytestostr(k)))
            print_nested_dict(v, prefix+"  ", "-", vformat=vformat, print_fn=print_fn,
                              version_keys=version_keys, hex_keys=hex_keys)
        else:
            sprint("%s%s %s : %s" % (prefix, lchar, bytestostr(k).ljust(l), vf(k, v)))

def reverse_dict(d):
    reversed_d = {}
    for k,v in d.items():
        reversed_d[v] = k
    return reversed_d


def std(s, extras="-,./: "):
    s = s or ""
    try:
        s = s.decode("latin1")
    except Exception:
        pass
    def c(v):
        try:
            return chr(v)
        except Exception:
            return str(v)
    def f(v):
        return str.isalnum(c(v)) or v in extras
    return "".join(filter(f, s))

def alnum(s):
    try:
        s = s.encode("latin1")
    except Exception:
        pass
    def c(v):
        try:
            return chr(v)
        except Exception:
            return str(v)
    def f(v):
        return str.isalnum(c(v))
    return "".join(c(v) for v in filter(f, s))

def nonl(x):
    if x is None:
        return None
    return str(x).replace("\n", "\\n").replace("\r", "\\r")

def xor(s1,s2):
    def _ord(v):
        try:
            return ord(v)
        except TypeError:
            return int(v)
    return ''.join(chr(_ord(a) ^ _ord(b)) for a,b in zip(s1,s2))

def engs(v):
    if isinstance(v, int):
        l = v
    else:
        try:
            l = len(v)
        except TypeError:
            return ""
    return "s" if l!=1 else ""


def obsc(v):
    OBSCURE_PASSWORDS = envbool("XPRA_OBSCURE_PASSWORDS", True)
    if OBSCURE_PASSWORDS:
        return "".join("*" for _ in (v or ""))
    return v


def csv(v):
    try:
        return ", ".join(str(x) for x in v)
    except Exception:
        return str(v)


def unsetenv(*varnames):
    for x in varnames:
        try:
            del os.environ[x]
        except KeyError:
            pass

def envint(name, d=0):
    try:
        return int(os.environ.get(name, d))
    except ValueError:
        return d

def envbool(name, d=False):
    try:
        v = os.environ.get(name)
        if v is None:
            return d
        return bool(int(v))
    except ValueError:
        return d

def envfloat(name, d=0):
    try:
        return float(os.environ.get(name, d))
    except ValueError:
        return d


#give warning message just once per key then ignore:
_once_only = set()
def first_time(key):
    global _once_only
    if key not in _once_only:
        _once_only.add(key)
        return True
    return False
