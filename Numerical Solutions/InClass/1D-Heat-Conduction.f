c 1D Heat Conduction Problem solved using C-N scheme
c         Ut =  Uxx
c         U(x,0) = exp(x)
c         U(0,t) = exp(t),U(1,t) = exp(1+t)
c The exact solution: U(x,t)= exp(x+t)

        dimension u1(0:10000),u2(0:10000),aa(0:10000),bb(0:10000)
        dimension ex(0:10000),vv(0:10000),be(0:10000),ar(0:10000)
        dimension err_w(0:1000000),x(0:10000),cc(0:10000),dd(0:10000)
        double precision u1,u2,aa,bb,cc,dd,be,ar,vv,ex,dx,dt,r,err,pi,x
c 16 digits  0D0

c parameters
        dt=0.5D-1
        dx=1D-3
c dx = h, r = mu
        r=dt/(dx*dx)
c	pi=3.14159265358979323846
        mx=1000
        n_end=20

c initial condition
        do i=0,mx
        x(i)=i*dx
        u1(i)=exp(x(i))
        enddo

c start computation
        nt=1
  1	    u2(0)=exp(nt*dt)
        u2(mx)=exp(1D0+nt*dt)

c set up tridiagonal system
        do i=1,mx-1
        aa(i)=1.0+r
        bb(i)=r/2D0
        cc(i)=bb(i)
        enddo
        do i=1,mx-1
        dd(i)=r*u1(i-1)/2D0+(1.0-r)*u1(i)+r*u1(i+1)/2D0
        enddo
        dd(1)=dd(1)+bb(1)*u2(0)
        dd(mx-1)=dd(mx-1)+cc(mx-1)*u2(mx)
        bb(1)=0D0
        cc(mx-1)=0D0

c Thomas algorithm
        be(0)=0.0
        ar(0)=0.0
        do k=1,mx-1
        be(k)=cc(k)/(aa(k)-bb(k)*be(k-1))
        ar(k)=(dd(k)+bb(k)*ar(k-1))/(aa(k)-bb(k)*be(k-1))
        enddo
        
        vv(mx)=0.0
        do j=1,mx-1
        jj=mx-j
        vv(jj)=be(jj)*vv(jj+1)+ar(jj)
        enddo
          
        do i=1,mx-1
        u2(i)=vv(i)
        enddo

c exact solution and error
        do i=0,mx
        ex(i)=exp(nt*dt+x(i))
        enddo
        err=0.0
        do i=1,mx-1
        err=err+(u2(i)-ex(i))*(u2(i)-ex(i))
        enddo
        err_w(nt)=sqrt(dx*err)
        print *, nt, err_w(nt)
        if(nt.eq.n_end)goto 2
        nt=nt+1
        do i=0,mx
        u1(i)=u2(i)
        enddo
        goto 1

c output
c find maximum error
  2     errmax=0.0
        do n=1,n_end
        if(err_w(n).gt.errmax)then
        errmax=err_w(n)
        endif
        enddo
        print *,"max error=", errmax
c output the solution
        open(unit=6,file='solution.data')
        print *,"max error=", errmax
        do i=0,mx
        write(6,3) i*dx,u2(i),ex(i)
        enddo
  3     format(f12.8,1x,f12.10,1x,f12.10)
        end
