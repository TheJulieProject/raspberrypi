cmd_/home/radu/Repos/raspberrypi/projects/drivers/system_timer.o :=  gcc-4.6 -Wp,-MD,/home/radu/Repos/raspberrypi/projects/drivers/.system_timer.o.d  -nostdinc -isystem /usr/lib/gcc/arm-linux-gnueabihf/4.6/include -I/usr/src/linux-headers-3.6-trunk-common/arch/arm/include -Iarch/arm/include/generated -Iinclude  -I/usr/src/linux-headers-3.6-trunk-common/include -include /usr/src/linux-headers-3.6-trunk-common/include/linux/kconfig.h   -I/home/radu/Repos/raspberrypi/projects/drivers -D__KERNEL__ -mlittle-endian   -I/usr/src/linux-headers-3.6-trunk-common/arch/arm/mach-bcm2708/include -Wall -Wundef -Wstrict-prototypes -Wno-trigraphs -fno-strict-aliasing -fno-common -Werror-implicit-function-declaration -Wno-format-security -fno-delete-null-pointer-checks -Os -marm -fno-dwarf2-cfi-asm -mabi=aapcs-linux -mno-thumb-interwork -funwind-tables -D__LINUX_ARM_ARCH__=6 -march=armv6 -mtune=arm1136j-s -msoft-float -Uarm -Wframe-larger-than=1024 -fno-stack-protector -Wno-unused-but-set-variable -fomit-frame-pointer -Wdeclaration-after-statement -Wno-pointer-sign -fno-strict-overflow -fconserve-stack  -DMODULE  -D"KBUILD_STR(s)=\#s" -D"KBUILD_BASENAME=KBUILD_STR(system_timer)"  -D"KBUILD_MODNAME=KBUILD_STR(system_timer)" -c -o /home/radu/Repos/raspberrypi/projects/drivers/.tmp_system_timer.o /home/radu/Repos/raspberrypi/projects/drivers/system_timer.c

source_/home/radu/Repos/raspberrypi/projects/drivers/system_timer.o := /home/radu/Repos/raspberrypi/projects/drivers/system_timer.c

deps_/home/radu/Repos/raspberrypi/projects/drivers/system_timer.o := \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/init.h \
    $(wildcard include/config/modules.h) \
    $(wildcard include/config/hotplug.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/compiler.h \
    $(wildcard include/config/sparse/rcu/pointer.h) \
    $(wildcard include/config/trace/branch/profiling.h) \
    $(wildcard include/config/profile/all/branches.h) \
    $(wildcard include/config/enable/must/check.h) \
    $(wildcard include/config/enable/warn/deprecated.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/compiler-gcc.h \
    $(wildcard include/config/arch/supports/optimized/inlining.h) \
    $(wildcard include/config/optimize/inlining.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/compiler-gcc4.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/types.h \
    $(wildcard include/config/uid16.h) \
    $(wildcard include/config/lbdaf.h) \
    $(wildcard include/config/arch/dma/addr/t/64bit.h) \
    $(wildcard include/config/phys/addr/t/64bit.h) \
    $(wildcard include/config/64bit.h) \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/types.h \
  /usr/src/linux-headers-3.6-trunk-common/include/asm-generic/int-ll64.h \
  arch/arm/include/generated/asm/bitsperlong.h \
  /usr/src/linux-headers-3.6-trunk-common/include/asm-generic/bitsperlong.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/posix_types.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/stddef.h \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/posix_types.h \
  /usr/src/linux-headers-3.6-trunk-common/include/asm-generic/posix_types.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/module.h \
    $(wildcard include/config/sysfs.h) \
    $(wildcard include/config/unused/symbols.h) \
    $(wildcard include/config/generic/bug.h) \
    $(wildcard include/config/kallsyms.h) \
    $(wildcard include/config/smp.h) \
    $(wildcard include/config/tracepoints.h) \
    $(wildcard include/config/tracing.h) \
    $(wildcard include/config/event/tracing.h) \
    $(wildcard include/config/ftrace/mcount/record.h) \
    $(wildcard include/config/module/unload.h) \
    $(wildcard include/config/constructors.h) \
    $(wildcard include/config/debug/set/module/ronx.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/list.h \
    $(wildcard include/config/debug/list.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/poison.h \
    $(wildcard include/config/illegal/pointer/value.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/const.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/stat.h \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/stat.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/time.h \
    $(wildcard include/config/arch/uses/gettimeoffset.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/cache.h \
    $(wildcard include/config/arch/has/cache/line/size.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/kernel.h \
    $(wildcard include/config/preempt/voluntary.h) \
    $(wildcard include/config/debug/atomic/sleep.h) \
    $(wildcard include/config/prove/locking.h) \
    $(wildcard include/config/ring/buffer.h) \
    $(wildcard include/config/numa.h) \
    $(wildcard include/config/compaction.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/sysinfo.h \
  /usr/lib/gcc/arm-linux-gnueabihf/4.6/include/stdarg.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/linkage.h \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/linkage.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/bitops.h \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/bitops.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/irqflags.h \
    $(wildcard include/config/trace/irqflags.h) \
    $(wildcard include/config/irqsoff/tracer.h) \
    $(wildcard include/config/preempt/tracer.h) \
    $(wildcard include/config/trace/irqflags/support.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/typecheck.h \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/irqflags.h \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/ptrace.h \
    $(wildcard include/config/cpu/endian/be8.h) \
    $(wildcard include/config/arm/thumb.h) \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/hwcap.h \
  /usr/src/linux-headers-3.6-trunk-common/include/asm-generic/bitops/non-atomic.h \
  /usr/src/linux-headers-3.6-trunk-common/include/asm-generic/bitops/fls64.h \
  /usr/src/linux-headers-3.6-trunk-common/include/asm-generic/bitops/sched.h \
  /usr/src/linux-headers-3.6-trunk-common/include/asm-generic/bitops/hweight.h \
  /usr/src/linux-headers-3.6-trunk-common/include/asm-generic/bitops/arch_hweight.h \
  /usr/src/linux-headers-3.6-trunk-common/include/asm-generic/bitops/const_hweight.h \
  /usr/src/linux-headers-3.6-trunk-common/include/asm-generic/bitops/lock.h \
  /usr/src/linux-headers-3.6-trunk-common/include/asm-generic/bitops/le.h \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/byteorder.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/byteorder/little_endian.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/swab.h \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/swab.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/byteorder/generic.h \
  /usr/src/linux-headers-3.6-trunk-common/include/asm-generic/bitops/ext2-atomic-setbit.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/log2.h \
    $(wildcard include/config/arch/has/ilog2/u32.h) \
    $(wildcard include/config/arch/has/ilog2/u64.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/printk.h \
    $(wildcard include/config/printk.h) \
    $(wildcard include/config/dynamic/debug.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/kern_levels.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/dynamic_debug.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/string.h \
    $(wildcard include/config/binary/printf.h) \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/string.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/errno.h \
  arch/arm/include/generated/asm/errno.h \
  /usr/src/linux-headers-3.6-trunk-common/include/asm-generic/errno.h \
  /usr/src/linux-headers-3.6-trunk-common/include/asm-generic/errno-base.h \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/div64.h \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/compiler.h \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/bug.h \
    $(wildcard include/config/bug.h) \
    $(wildcard include/config/thumb2/kernel.h) \
    $(wildcard include/config/debug/bugverbose.h) \
    $(wildcard include/config/arm/lpae.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/asm-generic/bug.h \
    $(wildcard include/config/generic/bug/relative/pointers.h) \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/cache.h \
    $(wildcard include/config/arm/l1/cache/shift.h) \
    $(wildcard include/config/aeabi.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/seqlock.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/spinlock.h \
    $(wildcard include/config/debug/spinlock.h) \
    $(wildcard include/config/generic/lockbreak.h) \
    $(wildcard include/config/preempt.h) \
    $(wildcard include/config/debug/lock/alloc.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/preempt.h \
    $(wildcard include/config/debug/preempt.h) \
    $(wildcard include/config/preempt/count.h) \
    $(wildcard include/config/preempt/notifiers.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/thread_info.h \
    $(wildcard include/config/compat.h) \
    $(wildcard include/config/debug/stack/usage.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/bug.h \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/thread_info.h \
    $(wildcard include/config/arm/thumbee.h) \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/fpstate.h \
    $(wildcard include/config/vfpv3.h) \
    $(wildcard include/config/iwmmxt.h) \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/domain.h \
    $(wildcard include/config/io/36.h) \
    $(wildcard include/config/cpu/use/domains.h) \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/barrier.h \
    $(wildcard include/config/cpu/32v6k.h) \
    $(wildcard include/config/cpu/xsc3.h) \
    $(wildcard include/config/cpu/fa526.h) \
    $(wildcard include/config/arch/has/barriers.h) \
    $(wildcard include/config/arm/dma/mem/bufferable.h) \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/outercache.h \
    $(wildcard include/config/outer/cache/sync.h) \
    $(wildcard include/config/outer/cache.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/stringify.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/bottom_half.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/spinlock_types.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/spinlock_types_up.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/lockdep.h \
    $(wildcard include/config/lockdep.h) \
    $(wildcard include/config/lock/stat.h) \
    $(wildcard include/config/prove/rcu.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/rwlock_types.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/spinlock_up.h \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/processor.h \
    $(wildcard include/config/have/hw/breakpoint.h) \
    $(wildcard include/config/mmu.h) \
    $(wildcard include/config/arm/errata/754327.h) \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/hw_breakpoint.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/rwlock.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/spinlock_api_up.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/atomic.h \
    $(wildcard include/config/arch/has/atomic/or.h) \
    $(wildcard include/config/generic/atomic64.h) \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/atomic.h \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/cmpxchg.h \
    $(wildcard include/config/cpu/sa1100.h) \
    $(wildcard include/config/cpu/sa110.h) \
    $(wildcard include/config/cpu/v6.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/asm-generic/cmpxchg-local.h \
  /usr/src/linux-headers-3.6-trunk-common/include/asm-generic/atomic-long.h \
  /usr/src/linux-headers-3.6-trunk-common/include/asm-generic/atomic64.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/math64.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/uidgid.h \
    $(wildcard include/config/uidgid/strict/type/checks.h) \
    $(wildcard include/config/user/ns.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/highuid.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/kmod.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/gfp.h \
    $(wildcard include/config/kmemcheck.h) \
    $(wildcard include/config/highmem.h) \
    $(wildcard include/config/zone/dma.h) \
    $(wildcard include/config/zone/dma32.h) \
    $(wildcard include/config/pm/sleep.h) \
    $(wildcard include/config/cma.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/mmzone.h \
    $(wildcard include/config/force/max/zoneorder.h) \
    $(wildcard include/config/memcg.h) \
    $(wildcard include/config/memory/hotplug.h) \
    $(wildcard include/config/sparsemem.h) \
    $(wildcard include/config/memory/isolation.h) \
    $(wildcard include/config/have/memblock/node/map.h) \
    $(wildcard include/config/discontigmem.h) \
    $(wildcard include/config/flat/node/mem/map.h) \
    $(wildcard include/config/no/bootmem.h) \
    $(wildcard include/config/have/memory/present.h) \
    $(wildcard include/config/have/memoryless/nodes.h) \
    $(wildcard include/config/need/node/memmap/size.h) \
    $(wildcard include/config/need/multiple/nodes.h) \
    $(wildcard include/config/have/arch/early/pfn/to/nid.h) \
    $(wildcard include/config/flatmem.h) \
    $(wildcard include/config/sparsemem/extreme.h) \
    $(wildcard include/config/have/arch/pfn/valid.h) \
    $(wildcard include/config/nodes/span/other/nodes.h) \
    $(wildcard include/config/holes/in/zone.h) \
    $(wildcard include/config/arch/has/holes/memorymodel.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/wait.h \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/current.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/threads.h \
    $(wildcard include/config/nr/cpus.h) \
    $(wildcard include/config/base/small.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/numa.h \
    $(wildcard include/config/nodes/shift.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/nodemask.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/bitmap.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/pageblock-flags.h \
    $(wildcard include/config/hugetlb/page.h) \
    $(wildcard include/config/hugetlb/page/size/variable.h) \
  include/generated/bounds.h \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/page.h \
    $(wildcard include/config/cpu/copy/v4wt.h) \
    $(wildcard include/config/cpu/copy/v4wb.h) \
    $(wildcard include/config/cpu/copy/feroceon.h) \
    $(wildcard include/config/cpu/copy/fa.h) \
    $(wildcard include/config/cpu/xscale.h) \
    $(wildcard include/config/cpu/copy/v6.h) \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/glue.h \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/pgtable-2level-types.h \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/memory.h \
    $(wildcard include/config/need/mach/memory/h.h) \
    $(wildcard include/config/page/offset.h) \
    $(wildcard include/config/dram/size.h) \
    $(wildcard include/config/dram/base.h) \
    $(wildcard include/config/have/tcm.h) \
    $(wildcard include/config/arm/patch/phys/virt.h) \
    $(wildcard include/config/phys/offset.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/sizes.h \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/mach-bcm2708/include/mach/memory.h \
    $(wildcard include/config/bcm2708/nol2cache.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/asm-generic/memory_model.h \
    $(wildcard include/config/sparsemem/vmemmap.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/asm-generic/getorder.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/memory_hotplug.h \
    $(wildcard include/config/memory/hotremove.h) \
    $(wildcard include/config/have/arch/nodedata/extension.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/notifier.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/mutex.h \
    $(wildcard include/config/debug/mutexes.h) \
    $(wildcard include/config/have/arch/mutex/cpu/relax.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/rwsem.h \
    $(wildcard include/config/rwsem/generic/spinlock.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/rwsem-spinlock.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/srcu.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/rcupdate.h \
    $(wildcard include/config/rcu/torture/test.h) \
    $(wildcard include/config/tree/rcu.h) \
    $(wildcard include/config/tree/preempt/rcu.h) \
    $(wildcard include/config/rcu/trace.h) \
    $(wildcard include/config/preempt/rcu.h) \
    $(wildcard include/config/tiny/rcu.h) \
    $(wildcard include/config/tiny/preempt/rcu.h) \
    $(wildcard include/config/debug/objects/rcu/head.h) \
    $(wildcard include/config/hotplug/cpu.h) \
    $(wildcard include/config/preempt/rt.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/cpumask.h \
    $(wildcard include/config/cpumask/offstack.h) \
    $(wildcard include/config/debug/per/cpu/maps.h) \
    $(wildcard include/config/disable/obsolete/cpumask/functions.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/completion.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/debugobjects.h \
    $(wildcard include/config/debug/objects.h) \
    $(wildcard include/config/debug/objects/free.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/rcutiny.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/workqueue.h \
    $(wildcard include/config/debug/objects/work.h) \
    $(wildcard include/config/freezer.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/timer.h \
    $(wildcard include/config/timer/stats.h) \
    $(wildcard include/config/debug/objects/timers.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/ktime.h \
    $(wildcard include/config/ktime/scalar.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/jiffies.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/timex.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/param.h \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/param.h \
    $(wildcard include/config/hz.h) \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/timex.h \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/arch_timer.h \
    $(wildcard include/config/arm/arch/timer.h) \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/mach-bcm2708/include/mach/timex.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/topology.h \
    $(wildcard include/config/sched/smt.h) \
    $(wildcard include/config/sched/mc.h) \
    $(wildcard include/config/sched/book.h) \
    $(wildcard include/config/use/percpu/numa/node/id.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/smp.h \
    $(wildcard include/config/use/generic/smp/helpers.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/percpu.h \
    $(wildcard include/config/need/per/cpu/embed/first/chunk.h) \
    $(wildcard include/config/need/per/cpu/page/first/chunk.h) \
    $(wildcard include/config/have/setup/per/cpu/area.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/pfn.h \
  arch/arm/include/generated/asm/percpu.h \
  /usr/src/linux-headers-3.6-trunk-common/include/asm-generic/percpu.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/percpu-defs.h \
    $(wildcard include/config/debug/force/weak/per/cpu.h) \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/topology.h \
    $(wildcard include/config/arm/cpu/topology.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/asm-generic/topology.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/mmdebug.h \
    $(wildcard include/config/debug/vm.h) \
    $(wildcard include/config/debug/virtual.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/sysctl.h \
    $(wildcard include/config/sysctl.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/rbtree.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/elf.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/elf-em.h \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/elf.h \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/user.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/kobject.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/sysfs.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/kobject_ns.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/kref.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/moduleparam.h \
    $(wildcard include/config/alpha.h) \
    $(wildcard include/config/ia64.h) \
    $(wildcard include/config/ppc64.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/tracepoint.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/static_key.h \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/jump_label.h \
    $(wildcard include/config/jump/label.h) \
  /usr/src/linux-headers-3.6-trunk-common/include/linux/export.h \
    $(wildcard include/config/symbol/prefix.h) \
    $(wildcard include/config/modversions.h) \
  /usr/src/linux-headers-3.6-trunk-common/arch/arm/include/asm/module.h \
    $(wildcard include/config/arm/unwind.h) \

/home/radu/Repos/raspberrypi/projects/drivers/system_timer.o: $(deps_/home/radu/Repos/raspberrypi/projects/drivers/system_timer.o)

$(deps_/home/radu/Repos/raspberrypi/projects/drivers/system_timer.o):
