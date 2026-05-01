! AI for Scientific Discovery and Computational Research
!
! Fortran example:
! Simple grid simulation for scientific computing and surrogate-model targets.
!
! Compile:
! gfortran grid_scientific_simulation.f90 -o grid_scientific_simulation
!
! Run:
! ./grid_scientific_simulation

program grid_scientific_simulation
  implicit none

  integer, parameter :: nx = 30
  integer, parameter :: ny = 30
  integer, parameter :: nt = 80
  real, parameter :: diffusion = 0.06
  real :: field(nx, ny)
  real :: next_field(nx, ny)
  integer :: i, j, t

  field = 0.0
  field(nx / 2, ny / 2) = 10.0

  do t = 1, nt
    next_field = field

    do i = 2, nx - 1
      do j = 2, ny - 1
        next_field(i, j) = field(i, j) + diffusion * ( &
          field(i + 1, j) + field(i - 1, j) + &
          field(i, j + 1) + field(i, j - 1) - &
          4.0 * field(i, j))
      end do
    end do

    field = next_field
  end do

  print *, "Final center value:", field(nx / 2, ny / 2)
  print *, "Final edge-adjacent value:", field(2, 2)

end program grid_scientific_simulation
