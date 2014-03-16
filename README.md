dogecoin-fedora
===============

# What

This is a repository of the files I use to build the dogecoin and related
utility packages hosted at <http://obsoleet.org/resources/dogecoin/>.

If you just want to use dogecoin on a Fedora 19 or 20 machine, please see the
link above.

If either you'd like to contribute, or you don't trust me, and would like to
verify and build packages for yourself, you're in the right spot.

# How

You'll need to do a bit of work to be able to build these packages.

## Required Utilities

- `mock` - A utility for building RPMs in a chroot, which verifies that the build
  process is not dependent on your normal system.
- `rpmdevtools` - Contains `spectool`, which is used for downloading upstream sources
- `createrepo` - Used to turn a directory of RPM packages into a repo

```bash
sudo yum install mock rpmdevtools createrepo
```

## Required Configuration

You'll need to add four new `mock` configs - One for each release and target
architecture. I've provided four example configurations in the `mock-configs`
directory. You should copy them to `/etc/mock`, then modify the last block in
each file to point at the filesystem path that you plan to have your repos at.

You can create the initial skeleton of repos in this directory using the
`createrepo` wrapper in this directory.

You'll also need to obtain the [ringingliberty
openssl-compat-bitcoin](http://linux.ringingliberty.com/bitcoin/) packages and
place them into the repos that your `mock` configs point at. I've included a
`build-openssl` script that will do this automatically.

## Building

For each package you'd like to build, you can use the `build` script. It takes
a single argument - the name of the package.

For instance, the following will build all four release/arch combinations of
the dogecoin packages:

```bash
./build dogecoin
```

# Donations

&ETH;OGE: DAphNjETW19XbvkXfihxwJaUtjJoK8cLxX
